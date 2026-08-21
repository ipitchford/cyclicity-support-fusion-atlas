#!/usr/bin/env python3
"""Derive the unified v0.7 body from the frozen v0.6 and v0.7 sources."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_SOURCE = ROOT / "ALL_DEGREE_GLOBAL_COMPLETION.md"
AMPLITUDE_SOURCE = ROOT / "AMPLITUDE_LAURENT_EXTENSION.md"
GLOBAL_OUTPUT = ROOT / "COMBINED_GLOBAL_COMPLETION.md"
AMPLITUDE_OUTPUT = ROOT / "COMBINED_AMPLITUDE_LAURENT.md"

SECTION_MAP = {str(index): str(index + 12) for index in range(1, 10)}
CODE_LITERALS = {"ALL_DEGREE_STRUCTURAL_REPAIR.md", "mullerthm"}


def typeset_inherited_inline_math(text: str) -> str:
    """Convert inherited mathematical code spans without touching source IDs."""

    nonzero_forms = {
        "(A,B)!=(0,0)": r"(A,B)\ \text{is nonzero}",
        "B=A^2/4!=0": r"B=A^2/4\in\mathbf C^\times",
    }

    def convert(match: re.Match[str]) -> str:
        expression = match.group(1)
        if expression in CODE_LITERALS:
            return match.group(0)
        expression = nonzero_forms.get(expression, expression)
        expression = expression.replace("!=0", r"\in\mathbf C^\times")
        expression = expression.replace("<=", r"\leq ")
        expression = expression.replace(">=", r"\geq ")
        expression = expression.replace("->", r"\longrightarrow ")
        expression = expression.replace(" circ ", r"\circ ")
        expression = expression.replace("...", r"\ldots ")
        expression = expression.replace("2|m", r"2\mid m")
        expression = expression.replace("<U,U^{-1}>", r"\langle U,U^{-1}\rangle")
        expression = expression.replace("|Gamma|", r"\lvert\Gamma\rvert")
        expression = expression.replace(
            "epsilon_gamma^k f_k", r"\epsilon_\gamma^k f_k"
        )
        expression = re.sub(r"\bGal\b", r"\\operatorname{Gal}", expression)
        expression = re.sub(r"\bker\b", r"\\ker", expression)
        expression = re.sub(r"\bdeg\b", r"\\deg", expression)
        expression = re.sub(r"\bdim\b", r"\\dim", expression)
        expression = re.sub(
            r"\b(PGL|PSL|AGL)_([A-Za-z0-9]+)",
            r"\\operatorname{\1}_{\2}",
            expression,
        )
        expression = re.sub(r"\b([AS])_([A-Za-z0-9]+)", r"\\mathrm{\1}_{\2}", expression)
        expression = re.sub(r"\bC_([A-Za-z0-9]+)", r"\\mathrm C_{\1}", expression)
        expression = re.sub(r"\bmu_", r"\\mu_", expression)
        for plain, tex in (
            ("Sigma", r"\Sigma"),
            ("Gamma", r"\Gamma"),
            ("lambda", r"\lambda"),
            ("epsilon", r"\epsilon"),
            ("omega", r"\omega"),
            ("zeta", r"\zeta"),
            ("chi", r"\chi"),
            ("tau", r"\tau"),
        ):
            expression = expression.replace(plain, tex)
        expression = re.sub(r"(?<![A-Za-z])C(?=[\[(]|$)", r"\\mathbf C", expression)
        expression = re.sub(r"(?<![A-Za-z])Z(?=[/]|$)", r"\\mathbf Z", expression)
        return rf"\({expression.strip()}\)"

    return re.sub(r"`([^`\n]+)`", convert, text)


def promote_global_headings(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("#### "):
            line = line[1:]
        elif line.startswith("### "):
            line = line[1:]
        elif line.startswith("## "):
            line = line[1:]
        lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def derive_global() -> str:
    source = GLOBAL_SOURCE.read_text(encoding="utf-8")
    start = source.index("## 1. Purpose and assurance boundary")
    end = source.index("## Sources used for imported classification steps")
    body = promote_global_headings(source[start:end])
    body = re.sub(r"(?m)^## Proof$", "### Proof", body)
    body = re.sub(
        r"The formal-moment isomorphism already proved in .*?identifies",
        (
            "The formal-moment construction in Theorem 14.1 below, applied "
            "to the constant amplitude, identifies"
        ),
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = body.replace(
        "- Laurent-polynomial, positive-characteristic, or arbitrary-amplitude\n"
        "  extensions.",
        (
            "- positive-characteristic extensions.\n\n"
            "Sections 13--19 below close the polynomial-amplitude and "
            "Laurent local-channel extensions. They preserve a separate "
            "boundary around a finite all-Laurent normal-form theorem."
        ),
    )
    body = body.replace(
        "Theorem 3.3 of Behajaina--Koenig--Neftin",
        "Theorem 3.3 of Behajaina--Koenig--Neftin [BKN26]",
    )
    body = body.replace(
        "Calbeto, *On the finite irreducible subgroups",
        "Calbeto [C25], *On the finite irreducible subgroups",
    )
    body = re.sub(
        r"The older source .Burda--Khovanskii., arXiv:1209\.5137",
        "The older source Burda--Khovanskii [BK16]",
        body,
    )
    body = body.replace(
        "Behajaina--Koenig--Neftin are exhaustive:",
        "Behajaina--Koenig--Neftin [BKN26] are exhaustive:",
    )
    body = body.replace(r"X_r\ne0", r"X_r\ \text{nonzero}")
    body = body.replace(
        r"U^m+V^m=-2b\ne0.",
        r"U^m+V^m=-2b,\qquad b\in\mathbf C^\times.",
    )
    body = body.replace(r"\qquad b\ne0.", r"\qquad b\in\mathbf C^\times.")
    body = body.replace(r"\qquad B\ne0.", r"\qquad B\in\mathbf C^\times.")
    body = typeset_inherited_inline_math(body)
    body = body.replace("\n\n\\(\\square\\)\n", " \\(\\square\\)\n")
    return (
        "<!-- Generated by tools/build_combined_sources.py; do not edit. -->\n\n"
        + body
    )


def remap_extension_numbers(text: str) -> str:
    def section_replacement(match: re.Match[str]) -> str:
        return f"# {SECTION_MAP[match.group(1)]}."

    def statement_replacement(match: re.Match[str]) -> str:
        return f"{match.group(1)} {SECTION_MAP[match.group(2)]}.{match.group(3)}"

    def tag_replacement(match: re.Match[str]) -> str:
        return rf"\tag{{{SECTION_MAP[match.group(1)]}.{match.group(2)}}}"

    def reference_replacement(match: re.Match[str]) -> str:
        return f"({SECTION_MAP[match.group(1)]}.{match.group(2)})"

    text = re.sub(r"(?m)^# ([1-9])\.", section_replacement, text)
    text = re.sub(
        r"\b(Theorem|Corollary|Example) ([1-9])\.(\d+)",
        statement_replacement,
        text,
    )
    text = re.sub(r"\\tag\{([1-9])\.(\d+)\}", tag_replacement, text)
    text = re.sub(r"\(([1-9])\.(\d+)\)", reference_replacement, text)
    return text


def derive_amplitude() -> str:
    source = AMPLITUDE_SOURCE.read_text(encoding="utf-8")
    start = source.index("# 1. Three notions of persistent vanishing")
    end = source.index("# References")
    body = remap_extension_numbers(source[start:end].rstrip() + "\n")
    body = re.sub(
        r"The formal moment isomorphism of \[EP3\] is reproduced in the form\s+needed here\.",
        "We construct the formal moment isomorphism in the form needed here.",
        body,
    )
    body = re.sub(
        r"Active Kummer components.*?Their cyclic rank is their number\.",
        (
            "For each active residue choose its leading power of s and write "
            "the corresponding exponent as alpha_r. Distinct residues give "
            "distinct alpha_r modulo the integers. The leading coefficient "
            "of the derivative Wronskian is the product of the nonzero "
            "channel coefficients and the Vandermonde product over the "
            "alpha_r. It is nonzero. The cyclic rank is therefore the number "
            "of active channels."
        ),
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = re.sub(
        (
            r"This section specialises Theorem 16\.1 using the all-degree\s+"
            r"normal forms and\s+right-factor audit of \[EP3\]\.\s+"
            r"Because \[EP3\] is unrefereed relative to named\s+"
            r"monodromy classifications, the same qualification attaches here\."
        ),
        (
            "Theorem 16.1 now specialises through the all-degree normal forms "
            "of Theorem 11.1 and the right-factor audit in Sections 7--9. "
            "Because Theorem 11.1 remains unrefereed relative to named "
            "monodromy classifications, the same qualification attaches here."
        ),
        body,
    )
    body = re.sub(
        (
            r"The endpoint table additionally imports \[PM09\] and the\s+"
            r"unrefereed\s+Atlas factor classification \[EP3\]\."
        ),
        (
            "The endpoint table additionally imports [PM09] and the "
            "unrefereed factor classification in Theorem 11.1."
        ),
        body,
    )
    if "[EP3" in body:
        contexts = [line for line in body.splitlines() if "[EP3" in line]
        raise RuntimeError(
            "combined amplitude body retained an EP3 self-citation: "
            + " | ".join(contexts)
        )
    return (
        "<!-- Generated by tools/build_combined_sources.py; do not edit. -->\n\n"
        + body
    )


def main() -> int:
    GLOBAL_OUTPUT.write_text(derive_global(), encoding="utf-8")
    AMPLITUDE_OUTPUT.write_text(derive_amplitude(), encoding="utf-8")
    print(GLOBAL_OUTPUT)
    print(AMPLITUDE_OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
