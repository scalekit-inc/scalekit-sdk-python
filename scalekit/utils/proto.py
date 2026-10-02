"""Conversions between protobuf well-known types and native Python values.

Lives here rather than at ``scalekit/util.py`` so it doesn't sit one typo
away from the pre-existing ``scalekit/utils/`` package.
"""
from typing import Any, Optional

from google.protobuf import struct_pb2


def _value_to_native(value: struct_pb2.Value) -> Any:
    """Convert a single google.protobuf.Value to its native Python form,
    recursing into struct/list values."""
    kind = value.WhichOneof("kind")
    if kind == "struct_value":
        return {
            key: _value_to_native(item)
            for key, item in value.struct_value.fields.items()
        }
    if kind == "list_value":
        return [_value_to_native(item) for item in value.list_value.values]
    # null_value, or a default Value with no kind set at all.
    if kind is None or kind == "null_value":
        return None
    # number_value (float), string_value (str), bool_value (bool).
    return getattr(value, kind)


def struct_to_dict(struct: Optional[struct_pb2.Struct]) -> Optional[dict]:
    """Fully (recursively) convert a google.protobuf.Struct to a native
    Python dict/list/scalar tree.

    ``dict(a_struct)`` -- the obvious thing to reach for -- only shallow
    converts. A Struct implements the Mapping protocol, so the top level
    looks right, but any nested Struct/ListValue *inside* it is handed
    back as a raw protobuf object rather than a plain dict/list. That is
    silently wrong for almost any real tool response, and it breaks the
    moment a call site JSON-encodes the result::

        json.dumps(dict(response.data))  # TypeError: Object of type
                                         # Struct is not JSON serializable

    Numbers come back as ``float``, never ``int``. This is not a choice
    this helper makes -- a Struct stores every number in
    ``Value.number_value``, which is a float64, so an upstream JSON
    ``{"id": 730994351}`` is already ``730994351.0`` by the time any SDK
    code sees it. ``dict(a_struct)`` has exactly the same behaviour.
    Integers beyond 2**53 are therefore not round-trippable.

    NaN and +/-Infinity are passed through as the corresponding Python
    floats. They are representable in a float64 and do arrive in practice
    (``json.loads`` accepts the bare ``NaN``/``Infinity`` literals, and
    ``1e400`` silently decodes to ``inf``), so this deliberately does not
    use ``json_format.MessageToDict``, which raises ``ValueError`` on
    them. Note that ``json.dumps`` will emit these as the non-standard
    ``NaN``/``Infinity`` literals unless you pass ``allow_nan=False``.

    Struct keys are map entries rather than declared proto fields, so
    they are never rewritten to camelCase and no
    ``preserving_proto_field_name`` handling is needed -- a key is
    returned exactly as the server sent it (e.g. ``input_schema``).

    :param struct: The Struct to convert, or None.
    :returns: A native dict, or None for an unset, empty or absent
        Struct. Empty and absent are deliberately not distinguished, so
        that the ``if response.data_dict:`` guard reads naturally; use
        ``response.HasField("data")`` when you need to tell a tool that
        returned ``{}`` from one that returned nothing at all.
    """
    if not struct:
        return None
    return {key: _value_to_native(item) for key, item in struct.fields.items()}


def register_struct_dict_property(message_cls, struct_field: str, name: str) -> None:
    """Attach a read-only ``<name>`` property to ``message_cls`` returning
    ``struct_to_dict`` of its ``struct_field``.

    Generated protobuf classes can't carry this in the ``.proto``, and a
    bare ``property`` assignment has a sharp edge: if ``name`` ever
    becomes a real generated field, the assignment succeeds, raises
    nothing, and has no effect -- the descriptor wins and every caller
    silently starts getting the raw field back. Warn rather than raise so
    that a future proto change can't break ``import scalekit`` outright
    for callers who never touch tools.
    """
    if name in message_cls.DESCRIPTOR.fields_by_name:
        import warnings

        warnings.warn(
            f"{message_cls.DESCRIPTOR.full_name} now has a real "
            f"'{name}' field; the Scalekit convenience property was not "
            f"registered and '{name}' returns the generated field "
            f"instead. Use scalekit.struct_to_dict({struct_field}) if you "
            f"need the converted dict.",
            RuntimeWarning,
            stacklevel=2,
        )
        return

    setattr(
        message_cls,
        name,
        property(lambda self: struct_to_dict(getattr(self, struct_field))),
    )
