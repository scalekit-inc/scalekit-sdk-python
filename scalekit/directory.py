from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.directories.directories_pb2 import *
from scalekit.v1.directories.directories_pb2_grpc import DirectoryServiceStub


class DirectoryClient:
    """ Class definition for Directory Client """

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Directory Client

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
        """
        Method to list directories

        :param organization_id  : org id to fetch directory list
        :type                   : ``` str ```
        
        :returns:
             list of directories
        """
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
        """
        Method to get directory based on given directory id and org id

        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param page_size         :     page size for org list fetch
        :type                    :     ``` int ```
        :param page_token        :     page token for org list fetch
        :type                    :     ``` str ```
        :param includeDetail     :     param to include detailed data
        :type                    :     ``` bool ```
        :param directoryGroupId  :     directory group id
        :type                    :     ``` str ```
        :param updatedAfter      :     param to get updated after detail
        :type                    :     ``` str ```

        :returns:
            Get Directory Response
        """
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
        """
        Method to fetch list of directory users

        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param page_size         :     page size for org list fetch
        :type                    :     ``` int ```
        :param page_token        :     page token for org list fetch
        :type                    :     ``` str ```
        :param includeDetail     :     param to include detailed data
        :type                    :     ``` bool ```
        :param updatedAfter      :     param to get updated after detail
        :type                    :     ``` str ```

        :returns:
             list of directory users
        """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectoryUsers.with_call,
            ListDirectoryUsersRequest(directory_id=directory_id, organization_id=organization_id),
        )

    def list_directory_groups(self, directory_id: str, organization_id: str) -> ListDirectoryGroupsResponse:
        """
        Method to fetch list of directory groups

        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param organization_id   :     Organization id
        :type                    :     ``` str ```

        :returns:
             list of directory groups
        """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectoryGroups.with_call,
            ListDirectoryGroupsRequest(directory_id=directory_id, organization_id=organization_id),
        )

    def enable_directory(self, directory_id: str, organization_id: str) -> ToggleDirectoryResponse:
        """
        Method to enable directory

        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param organization_id   :     Organization id
        :type                    :     ``` str ```

        :returns:
             Toggle Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.EnableDirectory.with_call,
            ToggleDirectoryRequest(id=directory_id, organization_id=organization_id),
        )

    def disable_directory(self, directory_id: str, organization_id: str) -> ToggleDirectoryResponse:
        """
        Method to disable directory

        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param organization_id   :     Organization id
        :type                    :     ``` str ```

        :returns:
             Toggle Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.DisableDirectory.with_call,
            ToggleDirectoryRequest(id=directory_id, organization_id=organization_id),
        )

    def get_primary_directory_by_organization_id(self, organization_id: str):
        """
        Method to get primary directory based on given organisation id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```

        :returns:
            response object for primary organization
        """
        response = self.core_client.grpc_exec(
            self.directory_service.ListDirectories.with_call,
            ListDirectoriesRequest(organization_id=organization_id),
        )

        if response:
            return response[0]
        else:
            raise Exception("directory does not exist for given organization")
