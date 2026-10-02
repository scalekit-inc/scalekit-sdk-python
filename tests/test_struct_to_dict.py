"""Unit tests for SK-1877: dict(struct) silently leaves nested fields as
raw protobuf objects.

Pure unit tests -- no live backend or credentials needed, unlike the rest
of tests/ (see BaseTest). Constructs Tool/ExecuteToolResponse/Struct
objects directly in-memory.
"""
import json
import math
import subprocess
import sys
import unittest
import warnings

from google.protobuf import struct_pb2

# Importing scalekit.tools (rather than just scalekit.v1.tools.tools_pb2)
# is what registers .data_dict/.definition_dict/.metadata_dict onto the
# generated classes. Today `import scalekit` reaches this module anyway
# via the client tree -- test_registration_requires_importing_scalekit
# below pins that, so a lazy-import refactor can't silently drop the
# properties while these tests keep passing.
import scalekit.tools  # noqa: F401
from scalekit.utils.proto import struct_to_dict
from scalekit.v1.tools.tools_pb2 import (
    ExecuteToolResponse,
    ListScopedToolsResponse,
    ScopedTool,
    Tool,
)


def _struct(d: dict) -> struct_pb2.Struct:
    s = struct_pb2.Struct()
    s.update(d)
    return s


class TestStructToDict(unittest.TestCase):
    """Direct tests of the struct_to_dict helper."""

    def test_none_returns_none(self):
        self.assertIsNone(struct_to_dict(None))

    def test_unset_struct_returns_none(self):
        self.assertIsNone(struct_to_dict(struct_pb2.Struct()))

    def test_flat_struct(self):
        s = _struct({"name": "github_search_issues", "score": 0.033, "ready": True})
        self.assertEqual(
            struct_to_dict(s),
            {"name": "github_search_issues", "score": 0.033, "ready": True},
        )

    def test_nested_object(self):
        s = _struct({"owner": {"login": "scalekit-inc", "id": 152854286}})
        result = struct_to_dict(s)
        self.assertIsInstance(result["owner"], dict)
        self.assertEqual(result["owner"]["login"], "scalekit-inc")

    def test_nested_list(self):
        s = _struct({"topics": ["agent-auth", "authentication", "docs"]})
        result = struct_to_dict(s)
        self.assertEqual(result, {"topics": ["agent-auth", "authentication", "docs"]})
        self.assertIsInstance(result["topics"], list)

    def test_list_of_objects(self):
        s = _struct({"items": [{"id": 1}, {"id": 2}]})
        result = struct_to_dict(s)
        self.assertTrue(all(isinstance(item, dict) for item in result["items"]))
        self.assertEqual([item["id"] for item in result["items"]], [1.0, 2.0])

    def test_deeply_nested_mixed_tree(self):
        """List inside object inside list inside object -- every level must
        come back native, not just the first."""
        s = _struct({
            "a": {"b": [{"c": {"d": ["leaf"]}}]},
        })
        result = struct_to_dict(s)
        self.assertEqual(result, {"a": {"b": [{"c": {"d": ["leaf"]}}]}})
        self.assertIsInstance(result["a"]["b"][0]["c"]["d"], list)

    def test_null_and_empty_containers(self):
        s = _struct({
            "license": None,
            "empty_object": {},
            "empty_list": [],
        })
        self.assertEqual(
            struct_to_dict(s),
            {"license": None, "empty_object": {}, "empty_list": []},
        )

    def test_result_is_json_serializable(self):
        """The load-bearing symptom of SK-1877. dict(struct) produces
        something json.dumps outright refuses; the helper must not."""
        s = _struct({"owner": {"login": "scalekit-inc"}, "topics": ["auth"]})

        with self.assertRaises(TypeError):
            json.dumps(dict(s))

        self.assertEqual(
            json.loads(json.dumps(struct_to_dict(s))),
            {"owner": {"login": "scalekit-inc"}, "topics": ["auth"]},
        )

    def test_dict_of_struct_leaves_nested_fields_as_protobuf(self):
        """Pins the bug being fixed, so it's obvious if a future protobuf
        release changes dict(struct) itself. Asserted on type rather than
        equality because a Struct is a Mapping and does compare equal to
        the dict it represents -- equality would pass either way."""
        s = _struct({"owner": {"login": "scalekit-inc"}, "topics": ["auth"]})
        shallow = dict(s)
        self.assertIsInstance(shallow["owner"], struct_pb2.Struct)
        self.assertIsInstance(shallow["topics"], struct_pb2.ListValue)

        result = struct_to_dict(s)
        self.assertIsInstance(result["owner"], dict)
        self.assertIsInstance(result["topics"], list)

    def test_struct_keys_are_returned_verbatim(self):
        """Struct keys are map entries, not declared proto fields, so they
        are never rewritten to camelCase -- a key comes back exactly as the
        server sent it, whatever its case."""
        s = _struct({"input_schema": {"displayProperties": {"read_only": True}}})
        result = struct_to_dict(s)
        self.assertEqual(
            result, {"input_schema": {"displayProperties": {"read_only": True}}}
        )

    def test_real_shaped_tool_response(self):
        """A GitHub repo shape: nested objects, a nested list, a null, and
        a deeply nested input-schema-like structure in one payload."""
        s = _struct({
            "id": 730994351,
            "full_name": "scalekit-inc/scalekit",
            "private": True,
            "license": None,
            "topics": ["agent-auth", "authentication"],
            "owner": {"login": "scalekit-inc", "id": 152854286, "type": "Organization"},
            "permissions": {"push": True, "admin": True, "pull": True},
        })
        result = struct_to_dict(s)
        self.assertEqual(result["full_name"], "scalekit-inc/scalekit")
        self.assertIsNone(result["license"])
        self.assertEqual(result["topics"], ["agent-auth", "authentication"])
        self.assertEqual(result["owner"]["login"], "scalekit-inc")
        self.assertTrue(result["permissions"]["admin"])
        json.dumps(result)  # must not raise


class TestNumericContract(unittest.TestCase):
    """A Struct stores every number in Value.number_value, a float64, so
    ints are already gone before any SDK code runs. Pinned explicitly
    because assertEqual alone cannot tell 1 from 1.0."""

    def test_integers_come_back_as_float(self):
        result = struct_to_dict(_struct({"id": 730994351, "count": 0}))
        self.assertIsInstance(result["id"], float)
        self.assertIsInstance(result["count"], float)
        self.assertEqual(result["id"], 730994351.0)

    def test_matches_dict_struct_numeric_behaviour(self):
        """Not a regression introduced by this helper: the shallow path
        callers used before produces the identical float."""
        s = _struct({"id": 730994351})
        self.assertEqual(struct_to_dict(s)["id"], dict(s)["id"])

    def test_large_integers_lose_precision(self):
        """Documents the float64 ceiling rather than pretending otherwise."""
        result = struct_to_dict(_struct({"n": 9007199254740993}))
        self.assertEqual(result["n"], 9007199254740992.0)

    def test_booleans_stay_bool_not_float(self):
        result = struct_to_dict(_struct({"admin": True, "archived": False}))
        self.assertIs(result["admin"], True)
        self.assertIs(result["archived"], False)


class TestNonFiniteNumbers(unittest.TestCase):
    """NaN/Infinity are representable in a float64 and do arrive in
    practice (json.loads accepts the bare literals; 1e400 decodes to inf).
    json_format.MessageToDict raises ValueError on them, which would make
    .data_dict crash where dict(.data) worked."""

    def test_infinity_passes_through(self):
        result = struct_to_dict(_struct({"score": float("inf")}))
        self.assertEqual(result["score"], float("inf"))

    def test_negative_infinity_passes_through(self):
        result = struct_to_dict(_struct({"score": float("-inf")}))
        self.assertEqual(result["score"], float("-inf"))

    def test_nan_passes_through(self):
        result = struct_to_dict(_struct({"score": float("nan")}))
        self.assertTrue(math.isnan(result["score"]))

    def test_nested_infinity_passes_through(self):
        result = struct_to_dict(_struct({"stats": {"ratios": [float("inf")]}}))
        self.assertEqual(result["stats"]["ratios"][0], float("inf"))

    def test_non_finite_does_not_raise_on_property_access(self):
        """A raising property is especially bad: it escapes plain attribute
        access and makes even hasattr() blow up instead of returning a
        bool. Guards like the hasattr checks in the framework adapters
        depend on this."""
        response = ExecuteToolResponse(data=_struct({"score": float("inf")}))
        self.assertTrue(hasattr(response, "data_dict"))
        self.assertEqual(response.data_dict["score"], float("inf"))

    def test_json_dumps_of_non_finite_needs_allow_nan_false_to_reject(self):
        """Documents the remaining sharp edge: stdlib json emits the
        non-standard Infinity literal by default."""
        result = struct_to_dict(_struct({"score": float("inf")}))
        self.assertEqual(json.dumps(result), '{"score": Infinity}')
        with self.assertRaises(ValueError):
            json.dumps(result, allow_nan=False)


class TestExecuteToolResponseDataDict(unittest.TestCase):
    """.data_dict on ExecuteToolResponse -- the property callers use."""

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
        json.dumps(result)  # must not raise

    def test_data_dict_when_data_unset(self):
        self.assertIsNone(ExecuteToolResponse().data_dict)

    def test_data_dict_when_data_present_but_empty(self):
        """A present-but-empty Struct also reports None, so that the
        `if response.data_dict:` guard reads naturally. Empty and absent
        are deliberately not distinguished here -- HasField("data") is the
        way to tell them apart, and this pins that choice so a future
        switch to presence-based semantics has to fail a test first."""
        response = ExecuteToolResponse(data=struct_pb2.Struct())
        self.assertTrue(response.HasField("data"))
        self.assertIsNone(response.data_dict)

    def test_data_dict_is_a_fresh_copy_each_access(self):
        """The property is computed, so mutating the result is a no-op on
        the message. Pinned so the behaviour is documented rather than
        discovered."""
        response = ExecuteToolResponse(data=_struct({"a": 1}))
        first = response.data_dict
        first["b"] = 2
        self.assertEqual(response.data_dict, {"a": 1.0})
        self.assertIsNot(response.data_dict, response.data_dict)

    def test_data_dict_reflects_later_writes_to_data(self):
        response = ExecuteToolResponse(data=_struct({"a": 1}))
        self.assertEqual(response.data_dict, {"a": 1.0})
        response.data["b"] = 2
        self.assertEqual(response.data_dict, {"a": 1.0, "b": 2.0})

    def test_data_dict_is_read_only(self):
        response = ExecuteToolResponse(data=_struct({"a": 1}))
        with self.assertRaises(AttributeError):
            response.data_dict = {"nope": True}

    def test_data_dict_survives_serialization_round_trip(self):
        original = ExecuteToolResponse(data=_struct({"owner": {"login": "sk"}}))
        revived = ExecuteToolResponse.FromString(original.SerializeToString())
        self.assertEqual(revived.data_dict, {"owner": {"login": "sk"}})


class TestToolDefinitionDict(unittest.TestCase):
    """.definition_dict / .metadata_dict on Tool."""

    def test_definition_dict_with_nested_input_schema(self):
        tool = Tool(definition=_struct({
            "name": "github_pull_requests_list",
            "input_schema": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "required": True},
                    "state": {"type": "string", "enum": ["open", "closed", "all"]},
                },
            },
        }))
        result = tool.definition_dict
        self.assertEqual(result["name"], "github_pull_requests_list")
        self.assertIsInstance(result["input_schema"]["properties"], dict)
        self.assertEqual(
            result["input_schema"]["properties"]["state"]["enum"],
            ["open", "closed", "all"],
        )
        json.dumps(result)  # must not raise

    def test_definition_dict_when_definition_unset(self):
        self.assertIsNone(Tool(provider="GITHUB").definition_dict)

    def test_metadata_dict_with_nested_payload(self):
        """Tool.metadata is the same Struct type with the same bug, so it
        gets the same treatment."""
        tool = Tool(metadata=_struct({"labels": {"tier": "beta"}, "tags": ["x"]}))
        self.assertEqual(
            tool.metadata_dict, {"labels": {"tier": "beta"}, "tags": ["x"]}
        )
        self.assertIsInstance(tool.metadata_dict["labels"], dict)

    def test_metadata_dict_when_metadata_unset(self):
        self.assertIsNone(Tool(provider="GITHUB").metadata_dict)


class TestNestedInListResponses(unittest.TestCase):
    """The access path the docstrings promise: the properties are on the
    generated classes, so they work on instances nested inside a list
    response, not just on top-level ones."""

    def test_definition_dict_on_tool_nested_in_scoped_tools_response(self):
        response = ListScopedToolsResponse(tools=[
            ScopedTool(
                identifier="user@example.com",
                tool=Tool(definition=_struct({
                    "name": "github_repos_get",
                    "input_schema": {"properties": {"owner": {"type": "string"}}},
                })),
            ),
        ])
        result = response.tools[0].tool.definition_dict
        self.assertEqual(result["name"], "github_repos_get")
        self.assertIsInstance(result["input_schema"]["properties"], dict)

    def test_scoped_tool_wrapper_has_no_definition_dict(self):
        """The property is on Tool, not on the ScopedTool wrapper -- worth
        pinning, since it's the easy mistake to make from the call site."""
        scoped = ScopedTool(tool=Tool(definition=_struct({"name": "x"})))
        self.assertFalse(hasattr(scoped, "definition_dict"))


class TestPropertyRegistration(unittest.TestCase):
    """The monkey-patching mechanism itself."""

    def test_registration_requires_importing_scalekit(self):
        """A bare `from scalekit.v1.tools.tools_pb2 import ...` gets the
        properties only because `import scalekit` eagerly builds the client
        tree and so reaches scalekit.tools. Run in a subprocess, since this
        module has already imported scalekit.tools. If a lazy-import
        refactor ever breaks the chain, this fails instead of the
        properties silently vanishing for real callers."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import scalekit\n"
                "from scalekit.v1.tools.tools_pb2 import ExecuteToolResponse, Tool\n"
                "assert hasattr(ExecuteToolResponse(), 'data_dict')\n"
                "assert hasattr(Tool(), 'definition_dict')\n"
                "assert hasattr(Tool(), 'metadata_dict')\n"
                "print('ok')\n",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)

    def test_struct_to_dict_is_exported_from_package_root(self):
        """The properties are invisible to type checkers because the
        generated .pyi declares __slots__, so the helper itself has to be
        reachable by name."""
        import scalekit

        self.assertIs(scalekit.struct_to_dict, struct_to_dict)
        self.assertIn("struct_to_dict", scalekit.__all__)

    def test_registration_warns_and_defers_on_name_collision(self):
        """Assigning a property over a name that IS a real generated field
        succeeds, raises nothing, and has no effect -- the descriptor wins.
        If the proto ever gains a real data_dict field, that must be loud
        rather than a silent no-op."""
        from scalekit.utils.proto import register_struct_dict_property

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            register_struct_dict_property(
                ExecuteToolResponse, "data", "execution_id"
            )

        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, RuntimeWarning)
        self.assertIn("execution_id", str(caught[0].message))
        # The real field is untouched.
        self.assertEqual(
            ExecuteToolResponse(execution_id="exec_1").execution_id, "exec_1"
        )


class TestBackwardCompatibility(unittest.TestCase):
    """Nothing about the existing public surface changed -- these are new
    attributes alongside the old ones, not replacements."""

    def test_data_field_itself_is_unchanged(self):
        response = ExecuteToolResponse(data=_struct({"a": 1}))
        self.assertIsInstance(response.data, struct_pb2.Struct)
        self.assertEqual(dict(response.data), {"a": 1})
        self.assertTrue(response.HasField("data"))

    def test_definition_and_metadata_fields_are_unchanged(self):
        tool = Tool(
            provider="GITHUB",
            definition=_struct({"name": "x"}),
            metadata=_struct({"tier": "beta"}),
        )
        self.assertIsInstance(tool.definition, struct_pb2.Struct)
        self.assertIsInstance(tool.metadata, struct_pb2.Struct)
        self.assertEqual(tool.definition["name"], "x")
        self.assertTrue(tool.HasField("definition"))

    def test_shallow_dict_pattern_still_works_for_flat_data(self):
        response = ExecuteToolResponse(data=_struct({"message": "ok"}))
        self.assertEqual(dict(response.data), {"message": "ok"})

    def test_messages_still_construct_with_no_arguments(self):
        self.assertIsInstance(ExecuteToolResponse(), ExecuteToolResponse)
        self.assertIsInstance(Tool(), Tool)

    def test_new_attributes_sit_alongside_the_originals(self):
        response = ExecuteToolResponse()
        tool = Tool()
        for obj, names in (
            (response, ("data", "data_dict")),
            (tool, ("definition", "definition_dict", "metadata", "metadata_dict")),
        ):
            for name in names:
                self.assertTrue(hasattr(obj, name), name)

    def test_frameworks_helper_still_returns_empty_dict_not_none(self):
        """scalekit.actions.frameworks.util.struct_to_dict keeps its own
        contract: {} rather than None for an empty Struct, because its
        callers go straight on to .get(...) on the result."""
        from scalekit.actions.frameworks.util import (
            struct_to_dict as frameworks_struct_to_dict,
        )

        self.assertEqual(frameworks_struct_to_dict(struct_pb2.Struct()), {})
        self.assertEqual(
            frameworks_struct_to_dict(_struct({"name": "x"})), {"name": "x"}
        )

    def test_frameworks_helper_still_accepts_a_whole_tool_message(self):
        """The same-named helpers are NOT interchangeable, and this is why
        they weren't consolidated: google_adk.py calls the frameworks one
        on an entire Tool message, not on a Struct field. The Struct-only
        helper cannot do that, so swapping them would break the Google ADK
        path with AttributeError: fields."""
        from scalekit.actions.frameworks.util import (
            struct_to_dict as frameworks_struct_to_dict,
        )

        tool = Tool(provider="GITHUB", definition=_struct({"name": "x"}))
        spec = frameworks_struct_to_dict(tool)
        self.assertEqual(spec["provider"], "GITHUB")
        self.assertEqual(spec["definition"], {"name": "x"})

        with self.assertRaises(AttributeError):
            struct_to_dict(tool)

    def test_google_adk_tool_conversion_path_still_works(self):
        """End-to-end over the shape google_adk.py builds, since that path
        needs an mcp install to import and so isn't otherwise covered."""
        from scalekit.actions.frameworks.util import (
            build_mcp_tool_from_spec,
            struct_to_dict as frameworks_struct_to_dict,
        )

        tool = Tool(provider="GITHUB", definition=_struct({
            "name": "github_repo_get",
            "description": "Get a repository.",
            "input_schema": {
                "type": "object",
                "properties": {"owner": {"type": "string"}},
                "required": ["owner"],
            },
            "annotations": {"title": "Get repo", "read_only_hint": True},
        }))
        mcp_tool = build_mcp_tool_from_spec(frameworks_struct_to_dict(tool))
        self.assertEqual(mcp_tool.name, "github_repo_get")
        # mcp 1.x exposes inputSchema/readOnlyHint, mcp 2.x renamed them to
        # input_schema/read_only_hint and keeps the old spelling only as a
        # constructor alias. Read whichever this install has.
        input_schema = getattr(mcp_tool, "input_schema", None)
        if input_schema is None:
            input_schema = mcp_tool.inputSchema
        self.assertEqual(input_schema["properties"], {"owner": {"type": "string"}})
        read_only = getattr(mcp_tool.annotations, "read_only_hint", None)
        if read_only is None:
            read_only = mcp_tool.annotations.readOnlyHint
        self.assertTrue(read_only)

    def test_frameworks_extract_tool_metadata_still_works(self):
        """The real caller of the delegating helper -- guards against the
        {} vs None contract change breaking it."""
        from scalekit.actions.frameworks.util import extract_tool_metadata

        name, description, definition_dict = extract_tool_metadata(
            Tool(provider="GITHUB", definition=_struct({
                "name": "github_repos_get",
                "description": "Get a repository.",
                "input_schema": {"properties": {"owner": {"type": "string"}}},
            }))
        )
        self.assertEqual(name, "github_repos_get")
        self.assertEqual(description, "Get a repository.")
        self.assertIsInstance(definition_dict["input_schema"], dict)

    def test_frameworks_extract_tool_metadata_falls_back_when_unset(self):
        from scalekit.actions.frameworks.util import extract_tool_metadata

        name, description, definition_dict = extract_tool_metadata(
            Tool(provider="GITHUB")
        )
        self.assertEqual(name, "GITHUB_tool")
        self.assertEqual(definition_dict, {})


if __name__ == "__main__":
    unittest.main()
