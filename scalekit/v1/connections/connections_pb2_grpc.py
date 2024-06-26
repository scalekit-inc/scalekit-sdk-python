# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from scalekit.v1.connections import connections_pb2 as scalekit_dot_v1_dot_connections_dot_connections__pb2


class ConnectionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/CreateConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionResponse.FromString,
                )
        self.GetConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/GetConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionResponse.FromString,
                )
        self.ListConnections = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/ListConnections',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsResponse.FromString,
                )
        self.UpdateConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/UpdateConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionResponse.FromString,
                )
        self.DeleteConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/DeleteConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.DeleteConnectionRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.EnableConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/EnableConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.FromString,
                )
        self.DisableConnection = channel.unary_unary(
                '/scalekit.v1.connections.ConnectionService/DisableConnection',
                request_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.FromString,
                )


class ConnectionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListConnections(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EnableConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisableConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ConnectionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionResponse.SerializeToString,
            ),
            'GetConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionResponse.SerializeToString,
            ),
            'ListConnections': grpc.unary_unary_rpc_method_handler(
                    servicer.ListConnections,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsResponse.SerializeToString,
            ),
            'UpdateConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionResponse.SerializeToString,
            ),
            'DeleteConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.DeleteConnectionRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'EnableConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.EnableConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.SerializeToString,
            ),
            'DisableConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.DisableConnection,
                    request_deserializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'scalekit.v1.connections.ConnectionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ConnectionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/CreateConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.CreateConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/GetConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.GetConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListConnections(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/ListConnections',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ListConnectionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/UpdateConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.UpdateConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/DeleteConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.DeleteConnectionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EnableConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/EnableConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisableConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.connections.ConnectionService/DisableConnection',
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionRequest.SerializeToString,
            scalekit_dot_v1_dot_connections_dot_connections__pb2.ToggleConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
