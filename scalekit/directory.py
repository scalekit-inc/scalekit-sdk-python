from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.directories.directories_pb2 import *
from scalekit.v1.directories.directories_pb2_grpc import DirectoryServiceStub


class DirectoryClient:
    """ """
    def __init__(self, core_client: CoreClient):
        """
        Initializer for Organization Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.directory_service = DirectoryServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_directories(self, organization_id) -> ListDirectoriesResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectories.with_call,
            ListDirectoriesRequest(organization_id=organization_id),
        )

    def get_directory(
            self,
            directory_id: str,
            organization_id: str,
            pageSize: Optional[int],
            pageToken: Optional[str],
            includeDetail: Optional[bool],
            directoryGroupId: Optional[str],
            updatedAfter: Optional[str]
    ) -> GetDirectoryResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.GetDirectory.with_call,
            GetDirectoryRequest(id=directory_id, organization_id=organization_id),
        )

    def list_directory_users(
            self,
            directory_id: str,
            organization_id: str,
            pageSize: Optional[int],
            pageToken: Optional[str],
            includeDetail: Optional[bool],
            updatedAfter: Optional[str]
    ) -> ListDirectoryUsersResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectoryUsers.with_call,
            ListDirectoryUsersRequest(directory_id=directory_id, organization_id=organization_id),
        )

    def list_directory_groups(self, directory_id: str, organization_id: str) -> ListDirectoryGroupsResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectoryGroups.with_call,
            ListDirectoryGroupsRequest(directory_id=directory_id, organization_id=organization_id),
        )

    def enable_directory(self, directory_id: str, organization_id: str) -> ToggleDirectoryResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.EnableDirectory.with_call,
            ToggleDirectoryRequest(id=directory_id, organization_id=organization_id),
        )

    def disable_directory(self, directory_id: str, organization_id: str) -> ToggleDirectoryResponse:
        """ """
        return self.core_client.grpc_exec(
            self.directory_service.DisableDirectory.with_call,
            ToggleDirectoryRequest(id=directory_id, organization_id=organization_id),
        )

    def get_primary_directory_by_organization_id(self, organization_id: str):
        """ """
        response = self.core_client.grpc_exec(
            self.directory_service.ListDirectories.with_call,
            ListDirectoriesRequest(organization_id=organization_id),
        )

        if response:
            return response[0]
        else:
            raise Exception("directory does not exist for given organization")
