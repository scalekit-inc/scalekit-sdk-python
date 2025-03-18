from typing import Optional, Any
from google.protobuf.json_format import MessageToJson

from scalekit.core import CoreClient
from scalekit.utils.directory import DirUser, ListDirUsersResponse, DirGroup, ListDirGroupsResponse

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

    def get_directory(
            self,
            organization_id: str,
            directory_id: str,
    ) -> GetDirectoryResponse:
        """
        Method to get directory based on given organization and directory id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param directory_id      :     directory id
        :type                    :     ``` str ```

        :returns:
            Get Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.GetDirectory.with_call,
            GetDirectoryRequest(
                id=directory_id,
                organization_id=organization_id,
            ),
        )

    def list_directories(self, organization_id) -> ListDirectoriesResponse:
        """
        Method to list directories for given organization id

        :param organization_id  : org id to fetch directory list
        :type                   : ``` str ```

        :returns:
             list of directories
        """
        return self.core_client.grpc_exec(
            self.directory_service.ListDirectories.with_call,
            ListDirectoriesRequest(organization_id=organization_id),
        )

    def list_directory_users(
            self,
            organization_id: str,
            directory_id: str,
            page_size: Optional[int] = None,
            page_token: Optional[str] = None,
            include_detail: Optional[bool] = None,
            updated_after: Optional[str] = None
    ) -> tuple[ListDirUsersResponse, Any]:
        """
        Method to fetch list of directory users based on given organization and directory id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param page_size         :     page size for org list fetch
        :type                    :     ``` int ```
        :param page_token        :     page token for org list fetch
        :type                    :     ``` str ```
        :param include_detail     :     param to include detailed data
        :type                    :     ``` bool ```
        :param updated_after      :     param to get updated after detail
        :type                    :     ``` str ```

        :returns:
             list of directory users
        """
        response = self.core_client.grpc_exec(
            self.directory_service.ListDirectoryUsers.with_call,
            ListDirectoryUsersRequest(
                organization_id=organization_id,
                directory_id=directory_id,
                page_size=page_size,
                page_token=page_token,
                include_detail=include_detail,
                updated_after=updated_after
            ),
        )

        user_response = (ListDirUsersResponse(), response[1])
        for user in response[0].users:
            dir_user = DirUser()
            dir_user.id = user.id
            dir_user.email = user.email
            dir_user.preferred_username = user.preferred_username
            dir_user.given_name = user.given_name
            dir_user.family_name = user.family_name
            dir_user.updated_at = user.updated_at
            dir_user.emails = user.emails
            dir_user.groups = user.groups
            dir_user.user_detail = MessageToJson(user.user_detail)

            if not hasattr(user_response[0], 'users'):
                user_response[0].users = [dir_user]
            else:
                user_response[0].users.append(dir_user)
            user_response[0].total_size = response[0].total_size
            user_response[0].next_page_token = response[0].next_page_token
            user_response[0].prev_page_token = response[0].prev_page_token

        return user_response

    def list_directory_groups(
            self,
            organization_id: str,
            directory_id: str,
            page_size: Optional[int] = None,
            page_token: Optional[str] = None,
            include_detail: Optional[bool] = None,
            updated_after: Optional[str] = None
    ) -> tuple[ListDirGroupsResponse, Any]:
        """
        Method to fetch list of directory groups based on given organization and directory id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param directory_id      :     directory id
        :type                    :     ``` str ```
        :param page_size         :     page size for org list fetch
        :type                    :     ``` int ```
        :param page_token        :     page token for org list fetch
        :type                    :     ``` str ```
        :param include_detail     :     param to include detailed data
        :type                    :     ``` bool ```
        :param updated_after      :     param to get updated after detail
        :type                    :     ``` str ```

        :returns:
             list of directory users
        """
        response = self.core_client.grpc_exec(
            self.directory_service.ListDirectoryGroups.with_call,
            ListDirectoryGroupsRequest(
                organization_id=organization_id,
                directory_id=directory_id,
                page_size=page_size,
                page_token=page_token,
                include_detail=include_detail,
                updated_after=updated_after
            ),
        )

        group_response = (ListDirGroupsResponse(), response[1])
        for group in response[0].groups:
            dir_group = DirGroup()
            dir_group.id = group.id
            dir_group.display_name = group.display_name
            dir_group.total_users = group.total_users
            dir_group.updated_at = group.updated_at
            dir_group.group_detail = MessageToJson(group.group_detail)

            if not hasattr(group_response, 'users'):
                group_response[0].groups = [dir_group]
            else:
                group_response[0].groups.append(dir_group)

            group_response[0].total_size = response[0].total_size
            group_response[0].next_page_token = response[0].next_page_token
            group_response[0].prev_page_token = response[0].prev_page_token

        return group_response

    def enable_directory(self, organization_id: str, directory_id: str) -> ToggleDirectoryResponse:
        """
        Method to enable directory based on given organization and directory id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param directory_id      :     directory id
        :type                    :     ``` str ```

        :returns:
             Toggle Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.EnableDirectory.with_call,
            ToggleDirectoryRequest(organization_id=organization_id, id=directory_id),
        )

    def disable_directory(self, organization_id: str, directory_id: str) -> ToggleDirectoryResponse:
        """
        Method to disable directory based on given organization and directory id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```
        :param directory_id      :     directory id
        :type                    :     ``` str ```

        :returns:
             Toggle Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.DisableDirectory.with_call,
            ToggleDirectoryRequest(organization_id=organization_id, id=directory_id),
        )

    def get_primary_directory_by_organization_id(self, organization_id: str):
        """
        Method to get primary directory based on given organization id

        :param organization_id   :     Organization id
        :type                    :     ``` str ```

        :returns:
            Primary directory
        """
        response = self.core_client.grpc_exec(
            self.directory_service.ListDirectories.with_call,
            ListDirectoriesRequest(organization_id=organization_id),
        )

        if response[0].directories:
            return response[0].directories[0]
        else:
            raise Exception("Directory does not exist for given Organization Id.")

    def create_directory(self, organization_id: str, directory: CreateDirectory) -> CreateDirectoryResponse:
        """
        Method to create directory based on given organization id

        :param organization_id   :     Organization id to create directory for
        :type                    :     ``` str ```
        :param directory         :     CreateDirectory object with expected values for dir creation
        :type                    :     ``` obj ```

        :returns:
            Create Directory Response
        """
        return self.core_client.grpc_exec(
            self.directory_service.CreateDirectory.with_call,
            CreateDirectoryRequest(organization_id=organization_id, directory=directory),
        )

    def delete_directory(self, organization_id: str, directory_id: str):
        """
        Method to delete directory based on given organization and directory id

        :param organization_id   :     Organization id to delete directory for
        :type                    :     ``` str ```
        :param directory_id      :     Directory id for directory to be deleted
        :type                    :     ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.directory_service.DeleteDirectory.with_call,
            DeleteDirectoryRequest(organization_id=organization_id, id=directory_id),
        )
