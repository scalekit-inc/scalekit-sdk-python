from typing import Optional, List, Dict

from scalekit.core import CoreClient
from scalekit.v1.clients.clients_pb2 import *
from scalekit.v1.clients.clients_pb2_grpc import ClientServiceStub


class M2MClient:
    """API to manage M2M client Authentication"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Organization M2M Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.client_service = ClientServiceStub(self.core_client.grpc_secure_channel)

    def create_organization_client(
        self, organization_id: str, m2m_client: OrganizationClient
    ) -> CreateOrganizationClientResponse:
        """
        Method to create organization client

        :param organization_id  : Organization Id to create client for
        :type                                 : ``` str ```
        :param m2m_client         : OrganizationClient obj with desired client properties defined
        :type                                 : ``` obj ```
        :returns:
             Create Organization Client Response
        """
        return self.core_client.grpc_exec(
            self.client_service.CreateOrganizationClient.with_call,
            CreateOrganizationClientRequest(organization_id=organization_id, client=m2m_client))

    def delete_organization_client(self, organization_id: str, client_id: str) -> None:
        """
        Method to delete organization client

        :param organization_id  : organization id
        :type                  : ``` str ```
        :param client_id        : client id
        :type                  : ``` str ```
        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.client_service.DeleteOrganizationClient.with_call,
            DeleteOrganizationClientRequest( organization_id=organization_id, client_id=client_id))
    
    def get_organization_client(self, organization_id: str, client_id: str) -> GetOrganizationClientResponse:
        """
        Method to get organization client

        :param organization_id  : organization id
        :type                  : ``` str ```
        :param client_id        : client id
        :type                  : ``` str ```
        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.client_service.GetOrganizationClient.with_call,
            GetOrganizationClientRequest(organization_id=organization_id, client_id=client_id))

    def update_organization_client(
            self, organization_id: str, client_id: str, m2m_client: OrganizationClient
    ) -> UpdateOrganizationClientResponse:
        """
        Method to update organization client
        :param organization_id  : organization id
        :type                  : ``` str ```
        :param client_id        : client id
        :type                  : ``` str ```
        :param m2m_client       :   Organization Client
        :type                               :   ``` Obj ```
        :returns:
            Update Organization Client Response
        """
        return self.core_client.grpc_exec(
            self.client_service.UpdateOrganizationClient.with_call,
            UpdateOrganizationClientRequest(organization_id=organization_id, client_id=client_id, client=m2m_client))

    def add_organization_client_secret(
            self, organization_id: str, client_id: str) -> CreateOrganizationClientSecretResponse:
        """
        Method to add organization client secret
        :param organization_id  : organization id
        :type                  : ``` str ```
        :param client_id        : client id
        :type                  : ``` str ```
        :returns:
            Create Organization Client Secret Response
        """
        return self.core_client.grpc_exec(
            self.client_service.CreateOrganizationClientSecret.with_call,
            CreateOrganizationClientSecretRequest(organization_id=organization_id, client_id=client_id))

    def remove_organization_client_secret(self, organization_id: str, client_id: str, secret_id: str) -> None:
        """
        Method to remove organization client secret
        :param organization_id  : organization id
        :type                  : ``` str ```
        :param client_id        : client id
        :type                  : ``` str ```
        :param secret_id        : secret id
        :type                  : ``` str ```
        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.client_service.DeleteOrganizationClientSecret.with_call,
            DeleteOrganizationClientSecretRequest(
                organization_id=organization_id, client_id=client_id, secret_id=secret_id)
        )

    def list_organization_clients(
        self, organization_id: str, page_size: Optional[int] = None, page_token: Optional[str] = None
    ) -> ListOrganizationClientsResponse:
        """
        Method to list organization clients

        :param organization_id  : Organization id to list clients for
        :type                   : ``` str ```
        :param page_size        : Page size for pagination (between 10 and 100)
        :type                   : ``` int ```
        :param page_token       : Page token for pagination
        :type                   : ``` str ```
        :returns:
            List Organization Clients Response
        """
        return self.core_client.grpc_exec(
            self.client_service.ListOrganizationClients.with_call,
            ListOrganizationClientsRequest(
                organization_id=organization_id,
                page_size=page_size,
                page_token=page_token
            )
        )
