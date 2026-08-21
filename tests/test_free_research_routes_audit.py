import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

import sys

sys.path.insert(0, str(TOOLS))

from run_free_research_routes_audit import PublicRouteClient


class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return b'{"ok": true}'


class FreeResearchRoutesAuditTests(unittest.TestCase):
    @patch("run_free_research_routes_audit.urlopen", return_value=FakeResponse())
    def test_authorization_header_is_used_but_never_logged(self, mocked_urlopen):
        client = PublicRouteClient()
        client.get_json(
            "OpenCitations Index",
            "https://example.test/citations",
            headers={"Authorization": "not-a-real-secret"},
        )

        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "not-a-real-secret")
        self.assertNotIn("not-a-real-secret", json.dumps(client.calls))

    @patch("run_free_research_routes_audit.urlopen")
    def test_provider_scoped_404_can_be_recorded_as_empty_result(self, mocked_urlopen):
        mocked_urlopen.side_effect = HTTPError(
            "https://example.test/search", 404, "Not Found", {}, io.BytesIO(b"{}")
        )
        client = PublicRouteClient()

        result = client.get_json(
            "zbMATH Open", "https://example.test/search", empty_404=True
        )

        self.assertEqual(result["status"]["nr_total_results"], 0)
        self.assertEqual(client.calls[0]["finding"], "empty_result")


if __name__ == "__main__":
    unittest.main()
