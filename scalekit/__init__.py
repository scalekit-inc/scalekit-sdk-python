
from scalekit.client import ScalekitClient
from scalekit.common.scalekit import CodeAuthenticationOptions, AuthorizationUrlOptions
from scalekit.utils.proto import struct_to_dict

__all__ = [
    'ScalekitClient',
    'AuthorizationUrlOptions',
    'CodeAuthenticationOptions',
    # Exported so the Struct conversion is reachable by name, and visible to
    # type checkers and IDEs. The generated tools_pb2.pyi stubs declare
    # __slots__, so a static checker cannot see the data_dict /
    # definition_dict / metadata_dict properties registered in tools.py and
    # will flag them as unknown attributes even though they work at runtime.
    'struct_to_dict',
]
