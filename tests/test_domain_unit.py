import unittest
from unittest.mock import Mock, patch
from scalekit.domain import DomainClient
from scalekit.v1.domains.domains_pb2 import DomainType, CreateDomain, CreateDomainRequest


class TestDomainUnit(unittest.TestCase):
    """Unit tests for domain functionality without requiring API credentials"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_core_client = Mock()
        self.domain_client = DomainClient(self.mock_core_client)

    def test_create_domain_with_allowed_email_domain_type(self):
        """Test create_domain method with ALLOWED_EMAIL_DOMAIN type"""
        # Arrange
        organization_id = "test_org_123"
        domain_name = "example.com"
        domain_type = DomainType.ALLOWED_EMAIL_DOMAIN
        
        # Mock the grpc_exec method
        self.mock_core_client.grpc_exec = Mock()
        
        # Act
        self.domain_client.create_domain(
            organization_id=organization_id,
            domain_name=domain_name,
            domain_type=domain_type
        )
        
        # Assert
        self.mock_core_client.grpc_exec.assert_called_once()
        call_args = self.mock_core_client.grpc_exec.call_args
        
        # Check that the request was created correctly
        request = call_args[0][1]  # Second argument is the request object
        self.assertIsInstance(request, CreateDomainRequest)
        self.assertEqual(request.organization_id, organization_id)
        
        # Check the domain object
        domain_obj = request.domain
        self.assertIsInstance(domain_obj, CreateDomain)
        self.assertEqual(domain_obj.domain, domain_name)
        self.assertEqual(domain_obj.domain_type, DomainType.ALLOWED_EMAIL_DOMAIN)

    def test_create_domain_with_organization_domain_type(self):
        """Test create_domain method with ORGANIZATION_DOMAIN type"""
        # Arrange
        organization_id = "test_org_123"
        domain_name = "example.com"
        domain_type = DomainType.ORGANIZATION_DOMAIN
        
        # Mock the grpc_exec method
        self.mock_core_client.grpc_exec = Mock()
        
        # Act
        self.domain_client.create_domain(
            organization_id=organization_id,
            domain_name=domain_name,
            domain_type=domain_type
        )
        
        # Assert
        self.mock_core_client.grpc_exec.assert_called_once()
        call_args = self.mock_core_client.grpc_exec.call_args
        
        # Check that the request was created correctly
        request = call_args[0][1]  # Second argument is the request object
        self.assertIsInstance(request, CreateDomainRequest)
        self.assertEqual(request.organization_id, organization_id)
        
        # Check the domain object
        domain_obj = request.domain
        self.assertIsInstance(domain_obj, CreateDomain)
        self.assertEqual(domain_obj.domain, domain_name)
        self.assertEqual(domain_obj.domain_type, DomainType.ORGANIZATION_DOMAIN)

    def test_create_domain_without_domain_type(self):
        """Test create_domain method without specifying domain_type (backward compatibility)"""
        # Arrange
        organization_id = "test_org_123"
        domain_name = "example.com"
        
        # Mock the grpc_exec method
        self.mock_core_client.grpc_exec = Mock()
        
        # Act
        self.domain_client.create_domain(
            organization_id=organization_id,
            domain_name=domain_name
        )
        
        # Assert
        self.mock_core_client.grpc_exec.assert_called_once()
        call_args = self.mock_core_client.grpc_exec.call_args
        
        # Check that the request was created correctly
        request = call_args[0][1]  # Second argument is the request object
        self.assertIsInstance(request, CreateDomainRequest)
        self.assertEqual(request.organization_id, organization_id)
        
        # Check the domain object
        domain_obj = request.domain
        self.assertIsInstance(domain_obj, CreateDomain)
        self.assertEqual(domain_obj.domain, domain_name)
        # When domain_type is not specified, it should be DOMAIN_TYPE_UNSPECIFIED (0)
        self.assertEqual(domain_obj.domain_type, DomainType.DOMAIN_TYPE_UNSPECIFIED)

    def test_domain_type_enum_values(self):
        """Test that DomainType enum values are correct"""
        self.assertEqual(DomainType.DOMAIN_TYPE_UNSPECIFIED, 0)
        self.assertEqual(DomainType.ALLOWED_EMAIL_DOMAIN, 1)
        self.assertEqual(DomainType.ORGANIZATION_DOMAIN, 2)


if __name__ == '__main__':
    unittest.main() 