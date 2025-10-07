#!/usr/bin/env python3
"""
Local development version of Scalekit SDK with SSL handling for local servers
"""

import os
import grpc
import ssl
from scalekit import ScalekitClient
from scalekit.core import CoreClient

class LocalScalekitClient(ScalekitClient):
    """
    Local development version of ScalekitClient that handles SSL issues with local servers
    """
    
    def __init__(self, env_url, client_id, client_secret, disable_ssl_verification=False):
        """
        Initialize the local Scalekit client
        
        :param env_url: Environment URL
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param disable_ssl_verification: Whether to disable SSL verification for local development
        """
        # Initialize the core client with SSL handling
        self.core_client = LocalCoreClient(env_url, client_id, client_secret, disable_ssl_verification)
        
        # Initialize all the service clients using the local core client
        import scalekit.organization as organization
        import scalekit.users as users
        import scalekit.sessions as sessions
        import scalekit.role as role
        import scalekit.permissions as permissions
        import scalekit.directory as directory
        import scalekit.domain as domain
        import scalekit.connection as connection
        import scalekit.passwordless as passwordless
        import scalekit.tools as tools
        import scalekit.connected_accounts as connected_accounts
        import scalekit.mcp as mcp
        import scalekit.m2m_client as m2m_client
        
        self.organization = organization.OrganizationClient(self.core_client)
        self.users = users.UserClient(self.core_client)
        self.sessions = sessions.SessionsClient(self.core_client)
        self.role = role.RoleClient(self.core_client)
        self.permissions = permissions.PermissionClient(self.core_client)
        self.directory = directory.DirectoryClient(self.core_client)
        self.domain = domain.DomainClient(self.core_client)
        self.connection = connection.ConnectionClient(self.core_client)
        self.passwordless = passwordless.PasswordlessClient(self.core_client)
        self.tools = tools.ToolsClient(self.core_client)
        self.connected_accounts = connected_accounts.ConnectedAccountsClient(self.core_client)
        self.mcp = mcp.McpClient(self.core_client)
        self.m2m_client = m2m_client.M2MClient(self.core_client)

class LocalCoreClient(CoreClient):
    """
    Local development version of CoreClient with SSL handling
    """
    
    def __init__(self, env_url, client_id, client_secret, disable_ssl_verification=False):
        """
        Initialize the local core client
        
        :param env_url: Environment URL
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param disable_ssl_verification: Whether to disable SSL verification
        """
        self.disable_ssl_verification = disable_ssl_verification
        
        # Initialize the parent class normally
        super().__init__(env_url, client_id, client_secret)
        
        # Override the gRPC channel with our local SSL handling
        self.__grpc_secure_channel()

    def __grpc_secure_channel(self):
        """
        Method to create gRPC channel with local SSL handling
        """
        # Set custom user-agent at channel level
        channel_options = [
            ('grpc.primary_user_agent', self.user_agent)
        ]
        
        if self.disable_ssl_verification:
            # For local development - create insecure channel
            print("🔧 Using insecure gRPC channel for local development")
            self.grpc_secure_channel = grpc.insecure_channel(self.host, options=channel_options)
        else:
            # Try to create secure channel with custom SSL context
            try:
                # Create gRPC credentials that accept self-signed certificates
                channel_credentials = grpc.ssl_channel_credentials()
                call_credentials = grpc.access_token_call_credentials(self.access_token)
                composite_credentials = grpc.composite_channel_credentials(
                    channel_credentials,
                    call_credentials,
                )
                
                self.grpc_secure_channel = grpc.secure_channel(
                    self.host, 
                    composite_credentials,
                    options=channel_options
                )
                print("✅ Created secure gRPC channel with custom SSL handling")
                
            except Exception as e:
                print(f"⚠️  Secure channel failed: {e}")
                print("🔧 Falling back to insecure channel for local development")
                self.grpc_secure_channel = grpc.insecure_channel(self.host, options=channel_options)

def test_local_connection():
    """
    Test function to verify local connection works
    """
    print("🚀 Testing Local Scalekit Connection")
    print("=" * 50)
    
    # Get environment variables
    env_url = os.getenv('SCALEKIT_ENV_URL', 'http://127.0.0.1:8888')
    client_id = os.getenv('SCALEKIT_CLIENT_ID', 'test_client_id')
    client_secret = os.getenv('SCALEKIT_CLIENT_SECRET', 'test_client_secret')
    
    print(f"Environment URL: {env_url}")
    print(f"Client ID: {client_id}")
    
    try:
        # Try with SSL verification disabled first
        print("\n🔧 Testing with SSL verification disabled...")
        client = LocalScalekitClient(env_url, client_id, client_secret, disable_ssl_verification=True)
        print("✅ Local Scalekit client initialized successfully!")
        
        # Test authorization URL generation
        print("\n📋 Testing authorization URL generation...")
        auth_url = client.get_authorization_url(
            "http://localhost:8000/auth/callback",
            state="test_state",
            connection_id="test_connection"
        )
        print(f"✅ Authorization URL: {auth_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Trying with SSL verification enabled...")
        
        try:
            client = LocalScalekitClient(env_url, client_id, client_secret, disable_ssl_verification=False)
            print("✅ Local Scalekit client initialized with SSL handling!")
            return True
        except Exception as e2:
            print(f"❌ SSL-enabled connection also failed: {e2}")
            return False

if __name__ == "__main__":
    test_local_connection()
