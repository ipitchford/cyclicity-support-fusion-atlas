#!/usr/bin/env python3
"""Build a dated, provider-separated open-index literature audit snapshot.

This is a discovery and citation-coverage receipt, not a novelty certificate.
It uses only documented public routes and deliberately keeps each provider's
result set separate so that index disagreement remains visible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


USER_AGENT = (
    "EvidencePress-CyclicityAudit/0.6 "
    "(https://evidencepress.org/releases/cyclicity-support-fusion-atlas/)"
)
REQUEST_INTERVAL_SECONDS = 0.55

ZBMATH_QUERIES = [
    '"fixed-seed cyclicity"',
    '"inverse-root support"',
    '"exponential Gauss-Manin" AND polynomial',
    '"polynomial monodromy" AND composition',
    "Gauss-Manin polynomial",
    "monodromy polynomial composition",
    '"polynomial moment problem"',
    '"linear relations" roots polynomial',
]

SEEDS = [
    {
        "key": "girstmair_root_relations",
        "title": "Linear relations between roots of polynomials",
        "doi": "10.4064/aa-89-1-53-96",
    },
    {
        "key": "pakovich_muzychuk_moment_problem",
        "title": "Solution of the polynomial moment problem",
        "doi": "10.1112/plms/pdp010",
    },
    {
        "key": "combot_root_relations",
        "title": "Computing linear relations between polynomial roots",
        "doi": "10.1090/mcom/4081",
    },
]


class PublicRouteClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self._last_request = 0.0

    def get_json(
        self,
        provider: str,
        url: str,
        *,
        empty_404: bool = False,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        delay = REQUEST_INTERVAL_SECONDS - (time.monotonic() - self._last_request)
        if delay > 0:
            time.sleep(delay)
        request_headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
        request_headers.update(headers or {})
        request = Request(url, headers=request_headers)
        started = time.monotonic()
        try:
            with urlopen(request, timeout=45) as response:
                status = response.status
                payload = response.read()
                content_type = response.headers.get("Content-Type", "")
            self._last_request = time.monotonic()
            record = {
                "provider": provider,
                "url": url,
                "http_status": status,
                "finding": "success",
                "bytes": len(payload),
                "content_type": content_type,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
            self.calls.append(record)
            return json.loads(payload)
        except HTTPError as exc:
            self._last_request = time.monotonic()
            if exc.code == 404 and empty_404:
                self.calls.append(
                    {
                        "provider": provider,
                        "url": url,
                        "http_status": exc.code,
                        "finding": "empty_result",
                        "elapsed_seconds": round(time.monotonic() - started, 3),
                    }
                )
                return {"status": {"nr_total_results": 0}, "result": []}
            finding = {
                401: "credential_rejected",
                403: "credential_missing",
                404: "not_in_source",
                429: "rate_limited",
            }.get(exc.code, "provider_fault" if exc.code >= 500 else "connector_failed")
            self.calls.append(
                {
                    "provider": provider,
                    "url": url,
                    "http_status": exc.code,
                    "finding": finding,
                    "retry_after": exc.headers.get("Retry-After"),
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                }
            )
            raise RuntimeError(f"{provider} returned HTTP {exc.code} ({finding})") from exc
        except (URLError, TimeoutError) as exc:
            self._last_request = time.monotonic()
            self.calls.append(
                {
                    "provider": provider,
                    "url": url,
                    "http_status": None,
                    "finding": "network_or_sandbox_block",
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                }
            )
            raise RuntimeError(f"{provider} network route failed") from exc


def canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def clean_title(value: Any) -> str | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if not isinstance(value, str):
        return None
    return " ".join(value.split())


def short_openalex_id(value: str | None) -> str | None:
    if not value:
        return None
    return value.rsplit("/", 1)[-1]


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    lowered = value.lower().strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lowered.startswith(prefix):
            return lowered[len(prefix) :]
    return lowered


def parse_oc_identifiers(value: str) -> dict[str, str]:
    identifiers: dict[str, str] = {}
    for token in value.split():
        if ":" not in token:
            continue
        scheme, identifier = token.split(":", 1)
        if scheme in {"doi", "openalex", "arxiv", "omid", "pmid"}:
            identifiers[scheme] = identifier
    return identifiers


def compact_zbmath_document(document: dict[str, Any]) -> dict[str, Any]:
    title = document.get("title") or {}
    links = document.get("links") or []
    return {
        "id": document.get("id"),
        "identifier": document.get("identifier"),
        "title": clean_title(title.get("title")),
        "year": document.get("year"),
        "authors": [
            author.get("name")
            for author in (document.get("contributors") or {}).get("authors", [])
            if author.get("name")
        ],
        "dois": sorted(
            {
                normalize_doi(link.get("identifier"))
                for link in links
                if link.get("type") == "doi" and link.get("identifier")
            }
        ),
        "zbmath_url": document.get("zbmath_url"),
    }


def zbmath_snapshot(client: PublicRouteClient) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for query in ZBMATH_QUERIES:
        url = "https://api.zbmath.org/v1/document/_search?" + urlencode(
            {"search_string": query, "results_per_page": 100}
        )
        payload = client.get_json("zbMATH Open", url, empty_404=True)
        status = payload.get("status") or {}
        documents = payload.get("result") or []
        reported = status.get("nr_total_results")
        if reported != len(documents):
            raise RuntimeError(
                f"zbMATH pagination boundary changed for {query!r}: "
                f"reported={reported}, retrieved={len(documents)}"
            )
        rows.append(
            {
                "query": query,
                "reported": reported,
                "retrieved": len(documents),
                "finding": "empty_result" if not documents else "success",
                "records": [compact_zbmath_document(item) for item in documents],
            }
        )
    return rows


def openalex_seed(client: PublicRouteClient, seed: dict[str, str]) -> dict[str, Any]:
    doi_url = f"https://doi.org/{seed['doi']}"
    work_url = "https://api.openalex.org/works/" + quote(doi_url, safe=":/")
    work = client.get_json("OpenAlex", work_url)
    openalex_id = short_openalex_id(work.get("id"))
    if not openalex_id:
        raise RuntimeError(f"OpenAlex seed has no id: {seed['key']}")
    citations_url = "https://api.openalex.org/works?" + urlencode(
        {
            "filter": f"cites:{openalex_id}",
            "per-page": 200,
            "select": "id,doi,title,publication_year,type",
        }
    )
    citations = client.get_json("OpenAlex", citations_url)
    reported = (citations.get("meta") or {}).get("count")
    results = citations.get("results") or []
    if reported != len(results):
        raise RuntimeError(
            f"OpenAlex result set exceeds one-page receipt boundary for {seed['key']}: "
            f"reported={reported}, retrieved={len(results)}"
        )
    return {
        "seed": {
            "id": openalex_id,
            "doi": normalize_doi(work.get("doi")),
            "title": clean_title(work.get("title")),
            "publication_year": work.get("publication_year"),
            "cited_by_count": work.get("cited_by_count"),
            "updated_date": work.get("updated_date"),
        },
        "reported": reported,
        "retrieved": len(results),
        "records": [
            {
                "openalex": short_openalex_id(item.get("id")),
                "doi": normalize_doi(item.get("doi")),
                "title": clean_title(item.get("title")),
                "year": item.get("publication_year"),
                "type": item.get("type"),
            }
            for item in results
        ],
    }


def opencitations_seed(client: PublicRouteClient, seed: dict[str, str]) -> dict[str, Any]:
    encoded = quote(f"doi:{seed['doi']}", safe=":")
    url = f"https://api.opencitations.net/index/v2/citations/{encoded}"
    token = os.environ.get("OPENCITATIONS_ACCESS_TOKEN")
    rows = client.get_json(
        "OpenCitations Index",
        url,
        headers={"Authorization": token} if token else None,
    )
    if not isinstance(rows, list):
        raise RuntimeError(f"unexpected OpenCitations response for {seed['key']}")
    return {
        "reported": len(rows),
        "retrieved": len(rows),
        "records": [
            {
                "oci": row.get("oci"),
                "creation": row.get("creation"),
                "timespan": row.get("timespan"),
                "identifiers": parse_oc_identifiers(row.get("citing", "")),
            }
            for row in rows
        ],
    }


def semantic_scholar_seed(client: PublicRouteClient, seed: dict[str, str]) -> dict[str, Any]:
    identifier = quote(f"DOI:{seed['doi']}", safe=":")
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/"
        f"{identifier}/citations?"
        + urlencode(
            {
                "limit": 100,
                "fields": "paperId,title,year,externalIds,url",
            }
        )
    )
    token = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    payload = client.get_json(
        "Semantic Scholar",
        url,
        headers={"x-api-key": token} if token else None,
    )
    records = payload.get("data") or []
    if payload.get("next") is not None:
        raise RuntimeError(f"Semantic Scholar pagination required for {seed['key']}")
    return {
        "reported": len(records),
        "retrieved": len(records),
        "records": [
            {
                "paper_id": (item.get("citingPaper") or {}).get("paperId"),
                "doi": normalize_doi(
                    ((item.get("citingPaper") or {}).get("externalIds") or {}).get("DOI")
                ),
                "arxiv": ((item.get("citingPaper") or {}).get("externalIds") or {}).get("ArXiv"),
                "title": clean_title((item.get("citingPaper") or {}).get("title")),
                "year": (item.get("citingPaper") or {}).get("year"),
                "url": (item.get("citingPaper") or {}).get("url"),
            }
            for item in records
        ],
    }


def crossref_seed(client: PublicRouteClient, seed: dict[str, str]) -> dict[str, Any]:
    url = "https://api.crossref.org/works/" + quote(seed["doi"], safe="")
    payload = client.get_json("Crossref", url)
    message = payload.get("message") or {}
    return {
        "doi": normalize_doi(message.get("DOI")),
        "title": clean_title(message.get("title")),
        "type": message.get("type"),
        "reference_count": message.get("reference-count"),
        "is_referenced_by_count": message.get("is-referenced-by-count"),
        "relation": message.get("relation") or {},
    }


def citation_keys(record: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    if record.get("openalex"):
        keys.add("openalex:" + record["openalex"].lower())
    if record.get("doi"):
        keys.add("doi:" + normalize_doi(record["doi"]))
    if record.get("arxiv"):
        keys.add("arxiv:" + record["arxiv"].lower())
    return keys


def compare_graphs(openalex: dict[str, Any], opencitations: dict[str, Any], semantic: dict[str, Any]) -> dict[str, Any]:
    oa_keys = [citation_keys(item) for item in openalex["records"]]
    s2_keys = [citation_keys(item) for item in semantic["records"]]
    oc_keys = [
        {f"{scheme}:{identifier.lower()}" for scheme, identifier in item["identifiers"].items()}
        for item in opencitations["records"]
    ]

    def overlap(left: list[set[str]], right: list[set[str]]) -> int:
        return sum(1 for row in left if row and any(row & other for other in right))

    return {
        "openalex_records": len(oa_keys),
        "opencitations_records": len(oc_keys),
        "semantic_scholar_records": len(s2_keys),
        "openalex_rows_matching_opencitations": overlap(oa_keys, oc_keys),
        "opencitations_rows_matching_openalex": overlap(oc_keys, oa_keys),
        "openalex_rows_matching_semantic_scholar": overlap(oa_keys, s2_keys),
        "semantic_scholar_rows_matching_openalex": overlap(s2_keys, oa_keys),
        "interpretation": (
            "Provider-specific citation graphs; differing counts and partial overlaps are "
            "coverage evidence, not contradictions and not universal exhaustiveness."
        ),
    }


def build_snapshot() -> dict[str, Any]:
    client = PublicRouteClient()
    seed_results: dict[str, Any] = {}
    for seed in SEEDS:
        openalex = openalex_seed(client, seed)
        opencitations = opencitations_seed(client, seed)
        semantic = semantic_scholar_seed(client, seed)
        crossref = crossref_seed(client, seed)
        seed_results[seed["key"]] = {
            "identity": seed,
            "crossref": crossref,
            "openalex": openalex,
            "opencitations": opencitations,
            "semantic_scholar": semantic,
            "cross_index_comparison": compare_graphs(openalex, opencitations, semantic),
        }

    snapshot: dict[str, Any] = {
        "schema": "cyclicity-free-research-routes-audit-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Supplement the bounded novelty audit with documented free discovery, "
            "metadata, and citation routes."
        ),
        "providers": {
            "zbmath_open": {
                "route": "official public REST API",
                "documentation": "https://api.zbmath.org/",
                "data_terms": "CC-BY-SA-4.0 under the provider API terms",
            },
            "openalex": {
                "route": "official REST API; no-key request succeeded for this snapshot",
                "documentation": "https://help.openalex.org/",
            },
            "opencitations": {
                "route": "official REST API; free token encouraged but not required for this snapshot",
                "documentation": "https://opencitations.net/querying/",
                "data_terms": "CC0",
                "access_token_used": bool(os.environ.get("OPENCITATIONS_ACCESS_TOKEN")),
            },
            "semantic_scholar": {
                "route": "official Academic Graph REST API; no-key request succeeded for this snapshot",
                "documentation": "https://www.semanticscholar.org/product/api",
                "api_key_used": bool(os.environ.get("SEMANTIC_SCHOLAR_API_KEY")),
            },
            "crossref": {
                "route": "official REST API",
                "documentation": "https://www.crossref.org/documentation/retrieve-metadata/rest-api/",
            },
            "ams_mathscinet": {
                "route": "AMS Batch MR Lookup for bibliographic matching only",
                "documentation": "https://mathscinet.ams.org/mathscinet/help/mr_lookup_help.html",
                "finding": "paid_only_for_required_capability",
                "limitation": (
                    "The free tools do not expose a full topical MathSciNet search, reviews, "
                    "or a complete MathSciNet citation graph. Automated topical scraping was not attempted."
                ),
            },
            "google_scholar": {
                "finding": "not_in_source",
                "limitation": "No official public API; scraping was not attempted.",
            },
        },
        "zbmath_queries": zbmath_snapshot(client),
        "seeds": seed_results,
        "request_log": client.calls,
        "assurance_boundary": {
            "supports": [
                "reproducible public-route query counts",
                "provider-specific forward-citation inventories for the named DOI seeds",
                "bibliographic identity cross-checks",
                "explicit diagnosis of remaining access and coverage gaps",
            ],
            "does_not_support": [
                "an exhaustive literature search",
                "an exhaustive MathSciNet search",
                "complete citation-forward coverage across all indexes",
                "absence of prior work",
                "novelty or priority certification",
                "mathematical correctness",
            ],
        },
    }
    snapshot["snapshot_sha256"] = canonical_hash(snapshot)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    snapshot = build_snapshot()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": "pass",
                "output": str(args.output),
                "snapshot_sha256": snapshot["snapshot_sha256"],
                "requests": len(snapshot["request_log"]),
                "zbmath_queries": len(snapshot["zbmath_queries"]),
                "citation_seeds": len(snapshot["seeds"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
