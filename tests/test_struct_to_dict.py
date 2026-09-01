"""Unit tests for SK-1877: dict(struct) silently leaves nested fields as
raw protobuf objects. Pure unit tests -- no live backend/credentials
needed, unlike the rest of tests/ (see BaseTest). Constructs
Tool/ExecuteToolResponse/Struct objects directly in-memory.
"""
import unittest

from google.protobuf import struct_pb2

# Importing scalekit.tools (rather than just scalekit.v1.tools.tools_pb2)
# is required: that's where .data_dict/.definition_dict get registered
# onto the generated Tool/ExecuteToolResponse classes (see tools.py). Real
# SDK usage always imports this module (ScalekitClient always constructs a
# ToolsClient), so this mirrors how the properties actually become
# available in practice.
import scalekit.tools as tools_module
from scalekit.util import struct_to_dict
from scalekit.v1.tools.tools_pb2 import Tool, ExecuteToolResponse


def _struct(d: dict) -> struct_pb2.Struct:
    s = struct_pb2.Struct()
    s.update(d)
    return s


class TestStructToDict(unittest.TestCase):
    """Direct tests of the struct_to_dict helper."""

    def test_none_returns_none(self):
        self.assertIsNone(struct_to_dict(None))

    def test_unset_struct_returns_none(self):
        # An unset/default Struct() is falsy, matching `if response.data:`
        # truthiness checks already used throughout this SDK's callers.
        self.assertIsNone(struct_to_dict(struct_pb2.Struct()))

    def test_flat_struct(self):
        s = _struct({"name": "github_search_issues", "score": 0.033, "ready": True})
        self.assertEqual(
            struct_to_dict(s),
            {"name": "github_search_issues", "score": 0.033, "ready": True},
        )

    def test_nested_object(self):
        # This is exactly what dict(struct) gets wrong: a nested object
        # stays a raw Struct/Value instead of becoming a plain dict.
        s = _struct({"owner": {"login": "scalekit-inc", "id": 152854286}})
        result = struct_to_dict(s)
        self.assertEqual(result, {"owner": {"login": "scalekit-inc", "id": 152854286}})
        self.assertIsInstance(result["owner"], dict)

    def test_nested_list(self):
        s = _struct({"topics": ["agent-auth", "authentication", "docs"]})
        result = struct_to_dict(s)
        self.assertEqual(result, {"topics": ["agent-auth", "authentication", "docs"]})
        self.assertIsInstance(result["topics"], list)

    def test_list_of_objects(self):
        s = _struct({"items": [{"id": 1}, {"id": 2}]})
        result = struct_to_dict(s)
        self.assertEqual(result, {"items": [{"id": 1}, {"id": 2}]})
        self.assertTrue(all(isinstance(item, dict) for item in result["items"]))

    def test_real_shaped_tool_response(self):
        """A GitHub repo object shape -- nested object (owner), nested
        object (permissions), nested list (topics), null field (license),
        and a deeply nested input-schema-like structure -- all in one
        payload, mirroring the real crash found live."""
        s = _struct({
            "id": 730994351,
            "full_name": "scalekit-inc/scalekit",
            "private": True,
            "license": None,
            "topics": ["agent-auth", "authentication"],
            "owner": {
                "login": "scalekit-inc",
                "id": 152854286,
                "type": "Organization",
            },
            "permissions": {
                "push": True,
                "admin": True,
                "pull": True,
            },
        })
        result = struct_to_dict(s)
        self.assertEqual(result["full_name"], "scalekit-inc/scalekit")
        self.assertIsNone(result["license"])
        self.assertEqual(result["topics"], ["agent-auth", "authentication"])
        self.assertIsInstance(result["owner"], dict)
        self.assertEqual(result["owner"]["login"], "scalekit-inc")
        self.assertIsInstance(result["permissions"], dict)
        self.assertTrue(result["permissions"]["admin"])

    def test_preserves_snake_case_field_names(self):
        # preserving_proto_field_name=True must be set -- otherwise a real
        # field like input_schema would come back as inputSchema, silently
        # breaking every existing lookup by the field's real name.
        s = _struct({"input_schema": {"display_properties": {"hidden": False}}})
        result = struct_to_dict(s)
        self.assertIn("input_schema", result)
        self.assertIn("display_properties", result["input_schema"])
        self.assertNotIn("inputSchema", result)

    def test_dict_of_struct_still_shallow_converts_by_contrast(self):
        """Documents the actual bug being fixed: plain dict(struct) leaves
        a nested object as a raw protobuf object, not a dict. This test
        exists to pin the bug's behavior so it's obvious if some future
        protobuf version changes it -- struct_to_dict must keep working
        regardless."""
        s = _struct({"owner": {"login": "scalekit-inc"}})
        shallow = dict(s)
        self.assertNotIsInstance(shallow["owner"], dict, "expected the known dict(struct) shallow-conversion gap")


class TestExecuteToolResponseDataDict(unittest.TestCase):
    """.data_dict on ExecuteToolResponse -- the property actually used by
    callers, wired through tools.py."""

    def test_data_dict_with_nested_payload(self):
        response = ExecuteToolResponse(data=_struct({
            "full_name": "scalekit-inc/scalekit",
            "owner": {"login": "scalekit-inc"},
            "topics": ["auth", "sso"],
        }))
        result = response.data_dict
        self.assertEqual(result["full_name"], "scalekit-inc/scalekit")
        self.assertIsInstance(result["owner"], dict)
        self.assertEqual(result["topics"], ["auth", "sso"])

    def test_data_dict_when_data_unset(self):
        response = ExecuteToolResponse()
        self.assertIsNone(response.data_dict)

    def test_data_field_itself_is_unchanged(self):
        """Backward compatibility: .data must still be the exact same
        Struct type and behavior as before this fix -- data_dict is
        strictly additive."""
        response = ExecuteToolResponse(data=_struct({"a": 1}))
        self.assertIsInstance(response.data, struct_pb2.Struct)
        self.assertEqual(dict(response.data), {"a": 1})  # old shallow pattern still works for flat data
        self.assertTrue(response.HasField("data"))


class TestToolDefinitionDict(unittest.TestCase):
    """.definition_dict on Tool -- used when fetching real tool schemas
    (e.g. for prompting an LLM to generate code against a tool)."""

    def test_definition_dict_with_nested_input_schema(self):
        tool = Tool(
            provider="GITHUB",
            definition=_struct({
                "name": "github_pull_requests_list",
                "description": "List pull requests in a repository.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string", "required": True},
                        "state": {"type": "string", "enum": ["open", "closed", "all"]},
                    },
                },
            }),
        )
        result = tool.definition_dict
        self.assertEqual(result["name"], "github_pull_requests_list")
        self.assertIsInstance(result["input_schema"], dict)
        self.assertIsInstance(result["input_schema"]["properties"], dict)
        self.assertEqual(result["input_schema"]["properties"]["state"]["enum"], ["open", "closed", "all"])

    def test_definition_dict_when_definition_unset(self):
        tool = Tool(provider="GITHUB")
        self.assertIsNone(tool.definition_dict)

    def test_definition_field_itself_is_unchanged(self):
        tool = Tool(provider="GITHUB", definition=_struct({"name": "x"}))
        self.assertIsInstance(tool.definition, struct_pb2.Struct)
        self.assertEqual(tool.definition["name"], "x")  # existing Struct.__getitem__ access still works


class TestBackwardCompatibility(unittest.TestCase):
    """Explicit checks that nothing about the existing public surface
    changed -- only new attributes were added."""

    def test_execute_tool_response_has_no_new_required_fields(self):
        # Constructing with zero args must still work exactly as before.
        response = ExecuteToolResponse()
        self.assertIsInstance(response, ExecuteToolResponse)

    def test_tool_has_no_new_required_fields(self):
        tool = Tool()
        self.assertIsInstance(tool, Tool)

    def test_existing_dict_conversion_pattern_unaffected_for_flat_data(self):
        # The exact pattern used in this repo's own runner.py today
        # (`str(dict(response.data))`) must keep behaving identically for
        # the flat-data case it was already working for.
        response = ExecuteToolResponse(data=_struct({"message": "ok"}))
        self.assertEqual(dict(response.data), {"message": "ok"})

    def test_data_dict_and_definition_dict_are_new_attributes_not_overrides(self):
        # Confirms these are additions, not replacements of existing
        # generated fields/methods. Protobuf message fields are only
        # visible via hasattr on an *instance* (descriptor magic at the C
        # level), not on the class itself -- hence constructing one here
        # rather than checking the class directly.
        response = ExecuteToolResponse()
        tool = Tool()
        self.assertTrue(hasattr(response, "data"))
        self.assertTrue(hasattr(response, "data_dict"))
        self.assertTrue(hasattr(tool, "definition"))
        self.assertTrue(hasattr(tool, "definition_dict"))


if __name__ == "__main__":
    unittest.main()
