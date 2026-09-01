"""Small standalone helpers shared across SDK modules."""
from typing import Optional

from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict


def struct_to_dict(struct: Optional[struct_pb2.Struct]) -> Optional[dict]:
    """Fully (recursively) convert a google.protobuf.Struct to a native
    Python dict/list/scalar tree.

    `dict(a_struct)` -- the obvious thing to reach for -- only shallow
    converts: a Struct implements the Mapping protocol, but any nested
    Struct/ListValue field inside it is handed back as a raw protobuf
    object, not a plain dict/list. That's silently wrong for almost any
    real-world tool response (nested objects, lists) and breaks call
    sites that stringify or JSON-encode the result -- e.g. a GitHub repo
    object's `owner`/`permissions`/`license` fields or a tool's
    `input_schema.properties`.

    This uses the canonical protobuf conversion (MessageToDict) with
    snake_case field names preserved, matching the field names already
    used elsewhere in this SDK (e.g. `input_schema`, not `inputSchema`).

    Returns None for an unset/empty Struct, matching the
    `if response.data:` truthiness checks already used throughout this
    SDK's own examples and callers.
    """
    if not struct:
        return None
    return MessageToDict(struct, preserving_proto_field_name=True)
