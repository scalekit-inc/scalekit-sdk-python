# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from scalekit.v1.users import users_pb2 as scalekit_dot_v1_dot_users_dot_users__pb2


class UserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateUser = channel.unary_unary(
                '/scalekit.v1.users.UserService/CreateUser',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserResponse.FromString,
                )
        self.UpdateUser = channel.unary_unary(
                '/scalekit.v1.users.UserService/UpdateUser',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserResponse.FromString,
                )
        self.GetUser = channel.unary_unary(
                '/scalekit.v1.users.UserService/GetUser',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.GetUserRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.GetUserResponse.FromString,
                )
        self.ListUsers = channel.unary_unary(
                '/scalekit.v1.users.UserService/ListUsers',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.ListUserRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.ListUserResponse.FromString,
                )
        self.DeleteUser = channel.unary_unary(
                '/scalekit.v1.users.UserService/DeleteUser',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.DeleteUserRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.AddUserToOrganization = channel.unary_unary(
                '/scalekit.v1.users.UserService/AddUserToOrganization',
                request_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.AddUserRequest.SerializeToString,
                response_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.AddUserResponse.FromString,
                )


class UserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddUserToOrganization(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateUser,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserResponse.SerializeToString,
            ),
            'UpdateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUser,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserResponse.SerializeToString,
            ),
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.GetUserRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.GetUserResponse.SerializeToString,
            ),
            'ListUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.ListUsers,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.ListUserRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.ListUserResponse.SerializeToString,
            ),
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.DeleteUserRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'AddUserToOrganization': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUserToOrganization,
                    request_deserializer=scalekit_dot_v1_dot_users_dot_users__pb2.AddUserRequest.FromString,
                    response_serializer=scalekit_dot_v1_dot_users_dot_users__pb2.AddUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'scalekit.v1.users.UserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/CreateUser',
            scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserRequest.SerializeToString,
            scalekit_dot_v1_dot_users_dot_users__pb2.CreateUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/UpdateUser',
            scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserRequest.SerializeToString,
            scalekit_dot_v1_dot_users_dot_users__pb2.UpdateUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/GetUser',
            scalekit_dot_v1_dot_users_dot_users__pb2.GetUserRequest.SerializeToString,
            scalekit_dot_v1_dot_users_dot_users__pb2.GetUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/ListUsers',
            scalekit_dot_v1_dot_users_dot_users__pb2.ListUserRequest.SerializeToString,
            scalekit_dot_v1_dot_users_dot_users__pb2.ListUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/DeleteUser',
            scalekit_dot_v1_dot_users_dot_users__pb2.DeleteUserRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddUserToOrganization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/scalekit.v1.users.UserService/AddUserToOrganization',
            scalekit_dot_v1_dot_users_dot_users__pb2.AddUserRequest.SerializeToString,
            scalekit_dot_v1_dot_users_dot_users__pb2.AddUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
