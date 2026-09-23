"""mcp is an optional dependency, needed only by the Google ADK adapter.

These tests run without credentials. They check that importing the SDK and
the shared framework helpers never loads mcp, and that the Google ADK adapter
points to the extra when mcp is missing.
"""

import importlib.util
import subprocess
import sys
import unittest

MCP_INSTALLED = importlib.util.find_spec("mcp") is not None


def _run(code: str) -> subprocess.CompletedProcess:
    # A fresh interpreter, so modules imported by other tests don't leak in.
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )


class TestOptionalMcp(unittest.TestCase):
    def test_core_imports_do_not_load_mcp(self):
        result = _run(
            "import sys\n"
            "import scalekit\n"
            "from scalekit import ScalekitClient\n"
            "import scalekit.actions.actions\n"
            "import scalekit.actions.frameworks.util\n"
            "print('mcp' in sys.modules)\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "False")

    @unittest.skipIf(MCP_INSTALLED, "mcp is installed; the missing-mcp path can't be exercised")
    def test_google_adk_without_mcp_points_to_extra(self):
        result = _run("import scalekit.actions.frameworks.google_adk")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pip install "scalekit-sdk-python[google-adk]"', result.stderr)

    @unittest.skipUnless(MCP_INSTALLED, "needs mcp: pip install 'scalekit-sdk-python[google-adk]'")
    def test_build_mcp_tool_from_spec(self):
        from scalekit.actions.frameworks.util import build_mcp_tool_from_spec

        tool = build_mcp_tool_from_spec(
            {
                "definition": {
                    "name": "gmail_fetch_mails",
                    "description": "Fetch emails",
                    "input_schema": {"type": "object", "properties": {}},
                    "annotations": {"read_only_hint": True},
                }
            }
        )
        self.assertEqual(tool.name, "gmail_fetch_mails")
        self.assertTrue(tool.annotations.readOnlyHint)


if __name__ == "__main__":
    unittest.main()
