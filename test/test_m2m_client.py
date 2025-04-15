import unittest
from unittest.mock import MagicMock, patch
from scalekit.m2m_client import M2MClient
from scalekit.core import CoreClient
from scalekit.v1.clients.clients_pb2_grpc import ClientServiceStub

# filepath: scalekit/test_m2m_client.py
from scalekit.v1.clients.clients_pb2 import (
    OrganizationClient,
    CreateOrganizationClientRequest,
    DeleteOrganizationClientRequest,
    GetOrganizationClientRequest,
    UpdateOrganizationClientRequest,
    CustomClaim,
    CreateOrganizationClientSecretRequest,
    DeleteOrganizationClientSecretRequest,
)


class TestM2MClient(unittest.TestCase):
    def setUp(self):
        self.mock_core_client = MagicMock(spec=CoreClient)
        self.mock_core_client.grpc_secure_channel = MagicMock()
        self.mock_core_client.grpc_exec = MagicMock()
        self.m2m_client = M2MClient(self.mock_core_client)

    def test_init(self):
        self.assertIsInstance(self.m2m_client.client_service, ClientServiceStub)

    def test_create_organization_client(self):
        m2m_client = OrganizationClient(name = "test_client", description= "test_description")
        organization_id = "org_123"
        self.m2m_client.create_organization_client(organization_id, m2m_client=m2m_client)
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.CreateOrganizationClient.with_call,
            CreateOrganizationClientRequest(organization_id=organization_id, client=m2m_client),
        )

    def test_delete_organization_client(self):
        organization_id = "org123"
        client_id = "client123"
        self.m2m_client.delete_organization_client(organization_id, client_id)
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.DeleteOrganizationClient.with_call,
            DeleteOrganizationClientRequest(
                organization_id=organization_id, client_id=client_id
            ),
        )

    def test_get_organization_client(self):
        organization_id = "org123"
        client_id = "client123"
        self.m2m_client.get_organization_client(organization_id, client_id)
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.GetOrganizationClient.with_call,
            GetOrganizationClientRequest(
                organization_id=organization_id, client_id=client_id
            ),
        )

    def test_update_organization_client(self):
        organization_id = "org123"
        client_id = "client123"
        claims = [ CustomClaim(key="user_type", value="admin"), CustomClaim(key="user_id", value="12345") ]
        m2m_client = OrganizationClient(name="test_client", description="Updated Description", custom_claims=claims)
        self.m2m_client.update_organization_client(
            organization_id, client_id, m2m_client
        )
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.UpdateOrganizationClient.with_call,
            UpdateOrganizationClientRequest(
                organization_id=organization_id,
                client_id=client_id,
                client=m2m_client,
            ),
        )

    def test_add_organization_client_secret(self):
        organization_id = "org123"
        client_id = "client123"
        self.m2m_client.add_organization_client_secret(organization_id, client_id)
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.CreateOrganizationClientSecret.with_call,
            CreateOrganizationClientSecretRequest(
                organization_id=organization_id, client_id=client_id
            ),
        )

    def test_remove_organization_client_secret(self):
        organization_id = "org123"
        client_id = "client123"
        secret_id = "secret123"
        self.m2m_client.remove_organization_client_secret(
            organization_id, client_id, secret_id
        )
        self.mock_core_client.grpc_exec.assert_called_once_with(
            self.m2m_client.client_service.DeleteOrganizationClientSecret.with_call,
            DeleteOrganizationClientSecretRequest(
                organization_id=organization_id,
                client_id=client_id,
                secret_id=secret_id,
            ),
        )


if __name__ == "__main__":
    unittest.main()