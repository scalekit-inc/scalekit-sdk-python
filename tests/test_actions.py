from basetest import BaseTest
from scalekit.actions.types import (
    ExecuteToolResponse,
    MagicLinkResponse,
    ListConnectedAccountsResponse,
    DeleteConnectedAccountResponse,
    GetConnectedAccountAuthResponse,
    CreateConnectedAccountResponse,
    UpdateConnectedAccountResponse,
    CreateMcpConfigResponse,
    UpdateMcpConfigResponse,
    ListMcpConfigsResponse,
    DeleteMcpConfigResponse,
    McpConfigConnectionToolMapping,
    EnsureMcpInstanceResponse,
    UpdateMcpInstanceResponse,
    GetMcpInstanceResponse,
    ListMcpInstancesResponse,
    DeleteMcpInstanceResponse,
    GetMcpInstanceAuthStateResponse,
)
from scalekit.actions.models.responses.get_connected_account_auth_response import ConnectedAccount
from scalekit.actions.modifier import Modifier

class TestConnect(BaseTest):
    """Class definition for Test Connect Class"""

    def setUp(self):
        """Setup test parameters"""
        self.test_identifier = "default"
        self.test_tool_name = "gmail_fetch_mails"
        self.test_connection_name = "GMAIL"
        self.test_basic_connection_name = "freshdesk-8"

        ca_response = self.scalekit_client.connect.get_connected_account(
            connection_name=self.test_connection_name,
            identifier=self.test_identifier
        )

        self.test_connected_account_id = ca_response.connected_account.id
        if ca_response.connected_account.status != "ACTIVE":
            response = self.scalekit_client.connect.get_authorization_link(identifier = self.test_identifier, connection_name="GMAIL")
            print(f"Authorization link: {response.link}")
            input("Press Enter to continue...")


    def test_execute_tool(self):
        """Method to test execute_tool with SLACK.SEND_MESSAGE"""
        tool_input = {
            "max_results": 1,
        }

        try:
            result = self.scalekit_client.actions.execute_tool(
                tool_input=tool_input,
                tool_name=self.test_tool_name,
                identifier=self.test_identifier,
            )
            # If successful, check response structure
            self.assertIsNotNone(result)
            self.assertIsInstance(result, ExecuteToolResponse)
            self.assertTrue(hasattr(result, 'data'))
            self.assertTrue(hasattr(result, 'execution_id'))
            self.assertIsNotNone(result.data)
        except Exception as e:
           raise e

    def test_execute_tool_invalid_tool(self):
        """Method to test execute_tool with invalid tool name"""
        tool_input = {
            "max_results": 1,
        }
        
        # Test with invalid tool name - should raise an exception
        with self.assertRaises(Exception) as context:
            self.scalekit_client.connect.execute_tool(
                tool_input=tool_input,
                tool_name="gmail_invalid_tool",  # Invalid tool name
                identifier=self.test_identifier,
            )
        
        # Verify the error contains expected invalid tool error message
        error_message = str(context.exception).lower()
        expected_errors = [
            "invalid tool",
            "tool not found", 
            "failed to get tool",
            "invalid argument"
        ]
        
        self.assertTrue(
            any(error in error_message for error in expected_errors),
            f"Expected invalid tool error, but got: {context.exception}"
        )


    def test_connect_client_initialization(self):
        """Method to test ConnectClient initialization"""
        self.assertTrue(hasattr(self.scalekit_client, 'connect'))
        self.assertIsNotNone(self.scalekit_client.connect)
        # Test that tools and connected_accounts dependencies are set
        self.assertEqual(
            self.scalekit_client.connect.tools,
            self.scalekit_client.tools
        )
        self.assertEqual(
            self.scalekit_client.connect.connected_accounts,
            self.scalekit_client.connected_accounts
        )

    def test_get_authorization_link_method_exists(self):
        """Method to test get_authorization_link method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'get_authorization_link'))
        self.assertTrue(callable(self.scalekit_client.connect.get_authorization_link))

    def test_get_authorization_link_response_structure(self):
        """Method to test get_authorization_link returns MagicLinkResponse"""
        try:
            result = self.scalekit_client.connect.get_authorization_link(
                connection_name="GMAIL",
                identifier=self.test_identifier
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, MagicLinkResponse)
            self.assertTrue(hasattr(result, 'link'))
            self.assertTrue(hasattr(result, 'expiry'))
        except Exception as e:
           raise e

    def test_list_connected_accounts_method_exists(self):
        """Method to test list_connected_accounts method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'list_connected_accounts'))
        self.assertTrue(callable(self.scalekit_client.connect.list_connected_accounts))

    def test_list_connected_accounts_response_structure(self):
        """Method to test list_connected_accounts returns ListConnectedAccountsResponse"""
        try:
            result = self.scalekit_client.connect.list_connected_accounts()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, ListConnectedAccountsResponse)
            self.assertTrue(hasattr(result, 'connected_accounts'))
            self.assertTrue(hasattr(result, 'total_count'))
            self.assertTrue(hasattr(result, 'next_page_token'))
            self.assertTrue(hasattr(result, 'previous_page_token'))
        except Exception as e:
           raise e

    def test_magic_link_response_structure(self):
        """Method to test MagicLinkResponse structure and methods"""
        from datetime import datetime
        
        # Test creating MagicLinkResponse directly
        response = MagicLinkResponse(
            link="https://example.com/auth/magic-link",
            expiry=datetime.now()
        )
        
        self.assertIsNotNone(response.link)
        self.assertIsNotNone(response.expiry)
        self.assertTrue(response.link.startswith("https://"))
        
        # Test to_dict method
        response_dict = response.to_dict()
        self.assertIsInstance(response_dict, dict)
        self.assertIn("link", response_dict)
        self.assertIn("expiry", response_dict)

    def test_magic_link_response_from_proto(self):
        """Method to test MagicLinkResponse.from_proto method"""
        from datetime import datetime
        
        # Create a mock proto-like object for testing
        class MockMagicLinkProto:
            def __init__(self):
                self.link = "https://test.com/magic-link"
                self.expiry = MockTimestamp()
        
        class MockTimestamp:
            def ToDatetime(self):
                return datetime.now()
        
        mock_proto = MockMagicLinkProto()
        response = MagicLinkResponse.from_proto(mock_proto)
        
        self.assertIsInstance(response, MagicLinkResponse)
        self.assertEqual(response.link, "https://test.com/magic-link")
        self.assertIsNotNone(response.expiry)


    def test_execute_tool_response_structure(self):
        """Method to test ExecuteToolResponse structure and methods"""
        # Test creating ExecuteToolResponse directly
        response = ExecuteToolResponse(
            data={"result": "success", "message_id": "12345"},
            execution_id="exec_123"
        )
        
        self.assertEqual(response.data["result"], "success")
        self.assertEqual(response.data["message_id"], "12345")
        self.assertEqual(response.execution_id, "exec_123")
        
        # Test to_dict method
        response_dict = response.to_dict()
        self.assertIsInstance(response_dict, dict)
        self.assertIn("data", response_dict)
        self.assertIn("execution_id", response_dict)
        self.assertEqual(response_dict["execution_id"], "exec_123")

    def test_delete_connected_account_method_exists(self):
        """Method to test delete_connected_account method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'delete_connected_account'))
        self.assertTrue(callable(self.scalekit_client.connect.delete_connected_account))


    def test_delete_connected_account(self):
        """Method to test delete_connected_account returns DeleteConnectedAccountResponse"""
        from scalekit.v1.connected_accounts.connected_accounts_pb2 import CreateConnectedAccount, AuthorizationDetails, OauthToken
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_delete_{uuid.uuid4().hex[:8]}"

        try:
            # First create a connected account to delete
            oauth_token = OauthToken(
                access_token="test_access_token",
                refresh_token="test_refresh_token",
                scopes=["read", "write"]
            )
            auth_details = AuthorizationDetails(oauth_token=oauth_token)
            connected_account = CreateConnectedAccount(authorization_details=auth_details)

            self.scalekit_client.connected_accounts.create_connected_account(
                connector="GMAIL",
                identifier=test_id,
                connected_account=connected_account
            )

            # Now delete the created connected account
            result = self.scalekit_client.connect.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, DeleteConnectedAccountResponse)
        except Exception as e:
            raise e

    def test_get_connected_account_auth_method_exists(self):
        """Method to test get_connected_account_auth method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'get_connected_account'))
        self.assertTrue(callable(self.scalekit_client.connect.get_connected_account))


    def test_get_connected_account_auth(self):
        """Method to test get_connected_account returns GetConnectedAccountAuthResponse"""
        try:
            result = self.scalekit_client.connect.get_connected_account(
                connection_name="GMAIL",
                identifier=self.test_identifier
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, GetConnectedAccountAuthResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            
            # Verify connected account structure
            connected_account = result.connected_account
            self.assertIsNotNone(connected_account)
            self.assertTrue(hasattr(connected_account, 'id'))
            self.assertTrue(hasattr(connected_account, 'identifier'))
            self.assertTrue(hasattr(connected_account, 'provider'))
            self.assertTrue(hasattr(connected_account, 'status'))
            self.assertTrue(hasattr(connected_account, 'authorization_type'))
            self.assertTrue(hasattr(connected_account, 'authorization_details'))
            
            # Verify OAuth details structure if present
            if connected_account.authorization_details and "oauth_token" in connected_account.authorization_details:
                oauth_token = connected_account.authorization_details["oauth_token"]
                self.assertIsInstance(oauth_token, dict)
                self.assertIn("access_token", oauth_token)
                self.assertIn("refresh_token", oauth_token)
                self.assertIn("scopes", oauth_token)
                self.assertIsInstance(oauth_token["scopes"], list)
                self.assertIsInstance(oauth_token["access_token"], str)
                self.assertIsInstance(oauth_token["refresh_token"], str)

        except Exception as e:
            raise e



    def test_execute_tool_with_connected_account_id(self):
        """Method to test execute_tool with connected_account_id parameter using dynamic ID"""
        
        tool_input = {
            "max_results": 1,
        }
        
        try:

            connected_account_response = self.scalekit_client.connect.get_connected_account(
                connection_name=self.test_connection_name,
                identifier=self.test_identifier,
            )

            
            # Now test execute_tool with connected_account_id
            result = self.scalekit_client.connect.execute_tool(
                tool_input=tool_input,
                tool_name=self.test_tool_name,
                connected_account_id=connected_account_response.connected_account.id
            )
            
            # If successful, check response structure
            self.assertIsNotNone(result)
            self.assertIsInstance(result, ExecuteToolResponse)
            self.assertTrue(hasattr(result, 'data'))
            self.assertTrue(hasattr(result, 'execution_id'))
            self.assertIsNotNone(result.data)
            
        except Exception as e:
            raise e

    def test_get_authorization_link_with_connected_account_id(self):
        """Method to test get_authorization_link with connected_account_id parameter"""
        try:

            connected_account_response = self.scalekit_client.connect.get_connected_account(
                connection_name=self.test_connection_name,
                identifier=self.test_identifier,
            )

            result = self.scalekit_client.connect.get_authorization_link(
                connection_name="GMAIL",
                connected_account_id=connected_account_response.connected_account.id
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, MagicLinkResponse)
            self.assertTrue(hasattr(result, 'link'))
            self.assertTrue(hasattr(result, 'expiry'))
        except Exception as e:
            raise e

    def test_delete_connected_account_with_connected_account_id(self):
        """Method to test delete_connected_account with connected_account_id parameter"""
        from scalekit.v1.connected_accounts.connected_accounts_pb2 import CreateConnectedAccount, AuthorizationDetails, OauthToken
        import uuid
        
        # Generate unique identifier for this test
        test_id = f"test_delete_id_{uuid.uuid4().hex[:8]}"
        
        try:
            # First create a connected account to delete
            oauth_token = OauthToken(
                access_token="test_access_token_id",
                refresh_token="test_refresh_token_id",
                scopes=["read", "write"]
            )
            auth_details = AuthorizationDetails(oauth_token=oauth_token)
            connected_account = CreateConnectedAccount(authorization_details=auth_details)
            
            create_response = self.scalekit_client.connected_accounts.create_connected_account(
                connector="GMAIL",
                identifier=test_id,
                connected_account=connected_account
            )
            
            # Extract the connected_account_id from the create response
            created_account_id = create_response[0].connected_account.id
            
            # Now delete the created connected account using the connected_account_id
            result = self.scalekit_client.connect.delete_connected_account(
                connected_account_id=created_account_id
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, DeleteConnectedAccountResponse)
        except Exception as e:
            raise e

    def test_get_connected_account_auth_with_connected_account_id(self):
        """Method to test get_connected_account_auth with connected_account_id parameter"""
        try:
            result = self.scalekit_client.connect.get_connected_account(
                connection_name="GMAIL",
                identifier=self.test_identifier,
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, GetConnectedAccountAuthResponse)
            self.assertTrue(hasattr(result, 'connected_account'))

        except Exception as e:
            raise e



    def test_get_modifiers_no_filter(self):
        """Test get_modifiers without filtering"""
        # Add test modifiers
        modifier1 = Modifier(tool_names="TOOL1", modifier_type="pre")
        modifier2 = Modifier(tool_names="TOOL2", modifier_type="post")
        
        self.scalekit_client.connect.add_modifier(modifier1)
        self.scalekit_client.connect.add_modifier(modifier2)
        
        # Get all modifiers
        modifiers = self.scalekit_client.connect.get_modifiers()
        self.assertEqual(len(modifiers), 2)


    # Tests for new create_connected_account functionality
    def test_create_connected_account_method_exists(self):
        """Method to test create_connected_account method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'create_connected_account'))
        self.assertTrue(callable(self.scalekit_client.connect.create_connected_account))

    def test_create_connected_account_with_oauth(self):
        """Method to test create_connected_account with OAuth authorization"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_create_oauth_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "scopes": ["read", "write"]
            }
        }

        try:
            result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)
            token = result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(token.get("access_token"), "test_access_token")
            self.assertEqual(token.get("refresh_token"), "test_refresh_token")
            self.assertEqual(token.get("scopes"), ["read", "write"])

            # Clean up - delete the created account
            self.scalekit_client.connect.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_create_connected_account_with_static_auth(self):
        """Method to test create_connected_account with static authorization"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_create_static_{uuid.uuid4().hex[:8]}"

        static_auth_details = {
            "static_auth": {
                "domain": "testdomain.freshdesk.com",
                "password": "testpassword",
                "username": "testusername"
            }
        }

        try:
            result = self.scalekit_client.connect.create_connected_account(
                connection_name=self.test_basic_connection_name,
                identifier=test_id,
                authorization_details=static_auth_details
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)
            auth = result.connected_account.authorization_details.get("static_auth", {})
            self.assertEqual(auth.get("domain"), "testdomain.freshdesk.com")
            self.assertEqual(auth.get("username"), "testusername")
            self.assertEqual(auth.get("password"), "testpassword")


            #Clean up - delete the created account
            self.scalekit_client.connect.delete_connected_account(
                connection_name=self.test_basic_connection_name,
                identifier=test_id
            )



        except Exception as e:
            raise e

    def test_create_connected_account_validation(self):
        """Method to test create_connected_account parameter validation"""
        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_token",
                "refresh_token": "test_refresh",
                "scopes": ["read"]
            }
        }

        # Test missing connection_name
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.connect.create_connected_account(
                connection_name="",
                identifier="test_id",
                authorization_details=oauth_auth_details
            )
        self.assertIn("connection_name is required", str(context.exception))

        # Test missing identifier
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.connect.create_connected_account(
                connection_name="GMAIL",
                identifier="",
                authorization_details=oauth_auth_details
            )
        self.assertIn("identifier is required", str(context.exception))


    # Tests for new get_or_create_connected_account functionality
    def test_get_or_create_connected_account_method_exists(self):
        """Method to test get_or_create_connected_account method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'get_or_create_connected_account'))
        self.assertTrue(callable(self.scalekit_client.connect.get_or_create_connected_account))

    def test_get_or_create_connected_account_get_existing(self):
        """Method to test get_or_create_connected_account returns existing account"""
        try:
            # Should get existing account
            result = self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=self.test_identifier
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, self.test_identifier)

        except Exception as e:
            raise e

    def test_get_or_create_connected_account_create_new(self):
        """Method to test get_or_create_connected_account creates new account when not found"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_get_or_create_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_get_or_create_token",
                "refresh_token": "test_get_or_create_refresh",
                "scopes": ["read", "write"]
            }
        }

        try:
            # Should create new account since it doesn't exist
            result = self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)

            # Now call it again - should get the existing account
            result2 = self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details
            )

            self.assertIsNotNone(result2)
            self.assertIsInstance(result2, CreateConnectedAccountResponse)
            self.assertEqual(result2.connected_account.identifier, test_id)
            self.assertEqual(result.connected_account.id, result2.connected_account.id)

            # Clean up - delete the created account
            self.scalekit_client.connect.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_get_or_create_connected_account_optional_auth_details(self):
        """Method to test get_or_create_connected_account with optional authorization_details"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_optional_auth_{uuid.uuid4().hex[:8]}"

        try:
            # Test with None authorization_details (should create with empty auth)
            result = self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details={
                    "oauth_token": {
                        "access_token": "",
                        "refresh_token": "",
                        "scopes": []
                    }
                }
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)

            # Test without authorization_details parameter (should use existing)
            result2 = self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(result2)
            self.assertIsInstance(result2, CreateConnectedAccountResponse)
            self.assertEqual(result2.connected_account.identifier, test_id)
            self.assertEqual(result.connected_account.id, result2.connected_account.id)

            # Clean up - delete the created account
            self.scalekit_client.connect.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_get_or_create_connected_account_validation(self):
        """Method to test get_or_create_connected_account parameter validation"""
        # Test missing connection_name
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="",
                identifier="test_id"
            )
        # The error will come from the get_connected_account call first

        # Test missing identifier
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.connect.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=""
            )
        # The error will come from the get_connected_account call first

    def test_create_connected_account_response_structure(self):
        """Method to test CreateConnectedAccountResponse structure"""
        # Test that response has expected structure
        from scalekit.actions.models.responses.create_connected_account_response import CreateConnectedAccountResponse
        from scalekit.actions.models.responses.get_connected_account_auth_response import ConnectedAccount

        # Create a mock ConnectedAccount
        mock_account = ConnectedAccount(
            id="test_id_123",
            identifier="test_identifier",
            provider="GMAIL",
            status="ACTIVE"
        )

        response = CreateConnectedAccountResponse(connected_account=mock_account)

        self.assertIsNotNone(response)
        self.assertTrue(hasattr(response, 'connected_account'))
        self.assertEqual(response.connected_account.identifier, "test_identifier")
        self.assertEqual(response.connected_account.provider, "GMAIL")

        # Test to_dict method
        response_dict = response.to_dict()
        self.assertIsInstance(response_dict, dict)
        self.assertIn("connected_account", response_dict)

    def test_create_connected_account_request_structure(self):
        """Method to test CreateConnectedAccountRequest structure"""
        from scalekit.actions.models.requests.create_connected_account_request import CreateConnectedAccountRequest

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_token",
                "refresh_token": "test_refresh",
                "scopes": ["read", "write"]
            }
        }

        request = CreateConnectedAccountRequest(
            connection_name="GMAIL",
            identifier="test_user",
            authorization_details=oauth_auth_details,
            organization_id="org_123",
            user_id="user_456"
        )

        self.assertEqual(request.connection_name, "GMAIL")
        self.assertEqual(request.identifier, "test_user")
        self.assertEqual(request.organization_id, "org_123")
        self.assertEqual(request.user_id, "user_456")
        self.assertIn("oauth_token", request.authorization_details)

        # Test proto conversion
        proto = request.to_proto()
        self.assertIsNotNone(proto)
        self.assertTrue(proto.authorization_details.HasField("oauth_token"))

        # Test empty auth details
        empty_request = CreateConnectedAccountRequest(
            connection_name="TEST",
            identifier="test_user"
        )

        self.assertEqual(empty_request.authorization_details, {})

        empty_proto = empty_request.to_proto()
        self.assertIsNotNone(empty_proto)
        self.assertTrue(empty_proto.authorization_details.HasField("oauth_token"))
        self.assertEqual(empty_proto.authorization_details.oauth_token.access_token, "")

    def test_google_adk_get_tools(self):

        google = self.scalekit_client.actions.google
        self.assertIsNotNone(google)

        from scalekit.actions.frameworks.google_adk import ScalekitGoogleAdkTool

        tools = google.get_tools(
            identifier=self.test_identifier,
            tool_names=["gmail_fetch_mails"],
            connection_names=["GMAIL"]
        )
        self.assertIsInstance(tools, list)
        self.assertGreaterEqual(len(tools), 1)
        self.assertIsInstance(tools[0], ScalekitGoogleAdkTool)
        print(tools)

    def test_langchain_adk_get_tools(self):

        lang = self.scalekit_client.actions.langchain
        self.assertIsNotNone(lang)

        tools = lang.get_tools(
            identifier=self.test_identifier,
            tool_names=["gmail_fetch_mails"],
            connection_names=["GMAIL"]
        )
        self.assertIsInstance(tools, list)
        self.assertGreaterEqual(len(tools), 1)
        print(tools)

    # API Config Tests for Existing Methods
    def test_create_connected_account_with_api_config(self):
        """Method to test create_connected_account with api_config parameter"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_create_api_config_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_access_token_api",
                "refresh_token": "test_refresh_token_api",
                "scopes": ["read", "write"]
            }
        }

        # Use connector-specific api_config fields that the server actually supports
        api_config = {
            "version": "v1",
            "domain": "gmail.com",
            "api_endpoint": "https://gmail.googleapis.com",
            "custom_auth_header": "Bearer"
        }

        try:
            result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=api_config
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)

            # Verify api_config is returned as a Python dictionary
            self.assertTrue(hasattr(result.connected_account, 'api_config'))
            self.assertIsNotNone(result.connected_account.api_config)
            self.assertIsInstance(result.connected_account.api_config, dict)

            # Verify expected api_config fields are present
            returned_config = result.connected_account.api_config
            expected_fields = ["version", "domain", "custom_headers", "custom_auth_header", "api_endpoint"]

            for field_name in expected_fields:
                self.assertIn(field_name, returned_config,
                              f"Expected field '{field_name}' not found in API config")

            # Verify our set values are preserved
            self.assertEqual(returned_config["version"], "v1")
            self.assertEqual(returned_config["domain"], "gmail.com")
            self.assertEqual(returned_config["api_endpoint"], "https://gmail.googleapis.com")
            self.assertEqual(returned_config["custom_auth_header"], "Bearer")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_get_or_create_connected_account_with_api_config(self):
        """Method to test get_or_create_connected_account with api_config parameter"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_get_or_create_api_config_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_get_or_create_api_token",
                "refresh_token": "test_get_or_create_api_refresh",
                "scopes": ["read", "write"]
            }
        }

        # Use connector-specific api_config fields
        api_config = {
            "version": "v2",
            "domain": "test.gmail.com",
            "api_endpoint": "https://test.gmail.googleapis.com",
            "custom_auth_header": "Token"
        }

        try:
            # Should create new account with api_config
            result = self.scalekit_client.actions.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=api_config
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateConnectedAccountResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
            self.assertIsNotNone(result.connected_account)
            self.assertEqual(result.connected_account.identifier, test_id)

            # Verify api_config was set correctly
            self.assertTrue(hasattr(result.connected_account, 'api_config'))
            self.assertIsNotNone(result.connected_account.api_config)
            self.assertIsInstance(result.connected_account.api_config, dict)

            returned_config = result.connected_account.api_config
            self.assertEqual(returned_config["version"], "v2")
            self.assertEqual(returned_config["domain"], "test.gmail.com")
            self.assertEqual(returned_config["api_endpoint"], "https://test.gmail.googleapis.com")
            self.assertEqual(returned_config["custom_auth_header"], "Token")

            # Now call it again - should get the existing account with same api_config
            result2 = self.scalekit_client.actions.get_or_create_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(result2)
            self.assertEqual(result2.connected_account.identifier, test_id)
            self.assertEqual(result.connected_account.id, result2.connected_account.id)

            # Verify existing account still has the api_config
            self.assertIsNotNone(result2.connected_account.api_config)
            self.assertEqual(result2.connected_account.api_config["version"], "v2")
            self.assertEqual(result2.connected_account.api_config["domain"], "test.gmail.com")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_api_config_response_structure(self):
        """Method to test api_config comes back as Python dictionary with correct field types"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_api_config_structure_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_structure_token",
                "refresh_token": "test_structure_refresh",
                "scopes": ["read"]
            }
        }

        # Use all supported api_config fields for GMAIL connector
        api_config = {
            "version": "v1.2",
            "domain": "structure.gmail.com",
            "api_endpoint": "https://structure.gmail.googleapis.com",
            "custom_auth_header": "Custom Bearer"
        }

        try:
            result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=api_config
            )

            self.assertIsNotNone(result.connected_account.api_config)
            returned_config = result.connected_account.api_config

            # Verify it's a Python dictionary, not protobuf Struct
            self.assertIsInstance(returned_config, dict)

            # Verify all expected fields are present
            expected_fields = ["version", "domain", "custom_headers", "custom_auth_header", "api_endpoint"]
            for field in expected_fields:
                self.assertIn(field, returned_config, f"Field '{field}' missing from api_config")

            # Verify field types and values we set
            self.assertIsInstance(returned_config["version"], str)
            self.assertEqual(returned_config["version"], "v1.2")

            self.assertIsInstance(returned_config["domain"], str)
            self.assertEqual(returned_config["domain"], "structure.gmail.com")

            self.assertIsInstance(returned_config["api_endpoint"], str)
            self.assertEqual(returned_config["api_endpoint"], "https://structure.gmail.googleapis.com")

            self.assertIsInstance(returned_config["custom_auth_header"], str)
            self.assertEqual(returned_config["custom_auth_header"], "Custom Bearer")

            # Verify custom_headers field (should be null/None or empty)
            # Note: protobuf null values might come back as None or empty values
            custom_headers = returned_config.get("custom_headers")
            # Just verify the field exists, value can be null/None/empty

            # Test dictionary access patterns work correctly
            self.assertEqual(returned_config.get("version"), "v1.2")
            self.assertEqual(returned_config.get("domain"), "structure.gmail.com")
            self.assertEqual(returned_config.get("nonexistent_field"), None)

            # Test that we can iterate over the dictionary
            field_count = 0
            for key, value in returned_config.items():
                field_count += 1
                self.assertIsInstance(key, str)
            self.assertGreater(field_count, 0)

            # Verify we can convert to JSON (important for serialization)
            import json
            json_str = json.dumps(returned_config)
            self.assertIsInstance(json_str, str)
            parsed_back = json.loads(json_str)
            self.assertEqual(parsed_back["version"], "v1.2")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    # Update Connected Account Tests
    def test_update_connected_account_method_exists(self):
        """Method to test update_connected_account method exists"""
        self.assertTrue(hasattr(self.scalekit_client.actions, 'update_connected_account'))
        self.assertTrue(callable(self.scalekit_client.actions.update_connected_account))

    def test_update_connected_account_with_oauth(self):
        """Method to test update_connected_account with OAuth authorization"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_oauth_{uuid.uuid4().hex[:8]}"

        # Initial OAuth auth details
        initial_oauth_auth_details = {
            "oauth_token": {
                "access_token": "initial_access_token",
                "refresh_token": "initial_refresh_token",
                "scopes": ["read"]
            }
        }

        # Updated OAuth auth details
        updated_oauth_auth_details = {
            "oauth_token": {
                "access_token": "updated_access_token",
                "refresh_token": "updated_refresh_token",
                "scopes": ["read", "write", "admin"]
            }
        }

        try:
            # First create a connected account
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=initial_oauth_auth_details
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Verify initial OAuth details
            initial_token = create_result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(initial_token.get("access_token"), "initial_access_token")
            self.assertEqual(initial_token.get("scopes"), ["read"])

            # Now update the connected account with new OAuth details
            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=updated_oauth_auth_details
            )

            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)
            self.assertTrue(hasattr(update_result, 'connected_account'))
            self.assertIsNotNone(update_result.connected_account)
            self.assertEqual(update_result.connected_account.identifier, test_id)

            # Verify updated OAuth details
            updated_token = update_result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(updated_token.get("access_token"), "updated_access_token")
            self.assertEqual(updated_token.get("refresh_token"), "updated_refresh_token")
            self.assertEqual(updated_token.get("scopes"), ["read", "write", "admin"])

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_update_connected_account_with_static_auth(self):
        """Method to test update_connected_account with static authorization"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_static_{uuid.uuid4().hex[:8]}"

        # Initial static auth details
        initial_static_auth_details = {
            "static_auth": {
                "domain": "initial.freshdesk.com",
                "username": "initial_user",
                "password": "initial_password"
            }
        }

        # Updated static auth details
        updated_static_auth_details = {
            "static_auth": {
                "domain": "updated.freshdesk.com",
                "username": "updated_user",
                "password": "updated_password"
            }
        }

        try:
            # First create a connected account with static auth
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name=self.test_basic_connection_name,  # freshdesk-8
                identifier=test_id,
                authorization_details=initial_static_auth_details
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Verify initial static auth details
            initial_auth = create_result.connected_account.authorization_details.get("static_auth", {})
            self.assertEqual(initial_auth.get("domain"), "initial.freshdesk.com")
            self.assertEqual(initial_auth.get("username"), "initial_user")
            self.assertEqual(initial_auth.get("password"), "initial_password")

            # Now update the connected account with new static auth details
            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name=self.test_basic_connection_name,  # freshdesk-8
                identifier=test_id,
                authorization_details=updated_static_auth_details
            )

            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)
            self.assertTrue(hasattr(update_result, 'connected_account'))
            self.assertIsNotNone(update_result.connected_account)
            self.assertEqual(update_result.connected_account.identifier, test_id)

            # Verify updated static auth details
            updated_auth = update_result.connected_account.authorization_details.get("static_auth", {})
            self.assertEqual(updated_auth.get("domain"), "updated.freshdesk.com")
            self.assertEqual(updated_auth.get("username"), "updated_user")
            self.assertEqual(updated_auth.get("password"), "updated_password")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name=self.test_basic_connection_name,
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_update_connected_account_with_api_config(self):
        """Method to test update_connected_account with api_config parameter"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_api_config_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_update_api_token",
                "refresh_token": "test_update_api_refresh",
                "scopes": ["read", "write"]
            }
        }

        # Initial API config
        initial_api_config = {
            "version": "v1.0",
            "domain": "initial.gmail.com",
            "api_endpoint": "https://initial.gmail.googleapis.com",
            "custom_auth_header": "Initial Bearer"
        }

        # Updated API config
        updated_api_config = {
            "version": "v2.0",
            "domain": "updated.gmail.com",
            "api_endpoint": "https://updated.gmail.googleapis.com",
            "custom_auth_header": "Updated Bearer"
        }

        try:
            # First create a connected account with initial API config
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=initial_api_config
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Verify initial API config
            self.assertIsNotNone(create_result.connected_account.api_config)
            initial_config = create_result.connected_account.api_config
            self.assertEqual(initial_config["version"], "v1.0")
            self.assertEqual(initial_config["domain"], "initial.gmail.com")

            # Now update the connected account with new API config
            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                api_config=updated_api_config
            )

            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)
            self.assertTrue(hasattr(update_result, 'connected_account'))
            self.assertIsNotNone(update_result.connected_account)
            self.assertEqual(update_result.connected_account.identifier, test_id)

            # Verify updated API config
            self.assertIsNotNone(update_result.connected_account.api_config)
            updated_config = update_result.connected_account.api_config
            self.assertEqual(updated_config["version"], "v2.0")
            self.assertEqual(updated_config["domain"], "updated.gmail.com")
            self.assertEqual(updated_config["api_endpoint"], "https://updated.gmail.googleapis.com")
            self.assertEqual(updated_config["custom_auth_header"], "Updated Bearer")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_update_connected_account_with_connected_account_id(self):
        """Method to test update_connected_account using connected_account_id parameter"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_ca_id_{uuid.uuid4().hex[:8]}"

        # Initial OAuth auth details
        initial_oauth_auth_details = {
            "oauth_token": {
                "access_token": "initial_ca_id_token",
                "refresh_token": "initial_ca_id_refresh",
                "scopes": ["read"]
            }
        }

        # Updated OAuth auth details
        updated_oauth_auth_details = {
            "oauth_token": {
                "access_token": "updated_ca_id_token",
                "refresh_token": "updated_ca_id_refresh",
                "scopes": ["read", "write"]
            }
        }

        try:
            # First create a connected account
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=initial_oauth_auth_details
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Get the connected_account_id for the update
            connected_account_id = create_result.connected_account.id
            self.assertIsNotNone(connected_account_id)

            # Verify initial OAuth details
            initial_token = create_result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(initial_token.get("access_token"), "initial_ca_id_token")
            self.assertEqual(initial_token.get("scopes"), ["read"])

            # Now update the connected account using connected_account_id instead of connection_name + identifier
            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",  # Still required in current implementation
                identifier=test_id,      # Still required in current implementation
                connected_account_id=connected_account_id,
                authorization_details=updated_oauth_auth_details
            )

            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)
            self.assertTrue(hasattr(update_result, 'connected_account'))
            self.assertIsNotNone(update_result.connected_account)
            self.assertEqual(update_result.connected_account.identifier, test_id)
            self.assertEqual(update_result.connected_account.id, connected_account_id)

            # Verify updated OAuth details
            updated_token = update_result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(updated_token.get("access_token"), "updated_ca_id_token")
            self.assertEqual(updated_token.get("refresh_token"), "updated_ca_id_refresh")
            self.assertEqual(updated_token.get("scopes"), ["read", "write"])

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_update_connected_account_validation(self):
        """Method to test update_connected_account validation and error handling"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_validation_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_validation_token",
                "refresh_token": "test_validation_refresh",
                "scopes": ["read"]
            }
        }

        try:
            # First create a connected account
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Test successful update with minimal parameters
            minimal_update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(minimal_update_result)
            self.assertIsInstance(minimal_update_result, UpdateConnectedAccountResponse)
            self.assertIsNotNone(minimal_update_result.connected_account)
            self.assertEqual(minimal_update_result.connected_account.identifier, test_id)

            # Test update with organization_id and user_id parameters
            update_with_ids_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                organization_id="test_org_id",
                user_id="test_user_id"
            )

            self.assertIsNotNone(update_with_ids_result)
            self.assertIsInstance(update_with_ids_result, UpdateConnectedAccountResponse)
            self.assertIsNotNone(update_with_ids_result.connected_account)
            self.assertEqual(update_with_ids_result.connected_account.identifier, test_id)

            # Test update with all valid parameters
            updated_auth_details = {
                "oauth_token": {
                    "access_token": "updated_validation_token",
                    "refresh_token": "updated_validation_refresh",
                    "scopes": ["read", "write"]
                }
            }

            api_config = {
                "version": "v1.1",
                "domain": "validation.gmail.com",
                "api_endpoint": "https://validation.gmail.googleapis.com",
                "custom_auth_header": "Validation Bearer"
            }

            full_update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=updated_auth_details,
                organization_id="test_org_id",
                user_id="test_user_id",
                connected_account_id=create_result.connected_account.id,
                api_config=api_config
            )

            self.assertIsNotNone(full_update_result)
            self.assertIsInstance(full_update_result, UpdateConnectedAccountResponse)
            self.assertIsNotNone(full_update_result.connected_account)
            self.assertEqual(full_update_result.connected_account.identifier, test_id)
            self.assertEqual(full_update_result.connected_account.id, create_result.connected_account.id)

            # Verify the updates were applied correctly
            updated_token = full_update_result.connected_account.authorization_details.get("oauth_token", {})
            self.assertEqual(updated_token.get("access_token"), "updated_validation_token")
            self.assertEqual(updated_token.get("scopes"), ["read", "write"])

            # Verify API config was updated
            self.assertIsNotNone(full_update_result.connected_account.api_config)
            updated_config = full_update_result.connected_account.api_config
            self.assertEqual(updated_config["version"], "v1.1")
            self.assertEqual(updated_config["domain"], "validation.gmail.com")

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_update_connected_account_response_structure(self):
        """Method to test update_connected_account response structure and types"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_update_structure_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_structure_token",
                "refresh_token": "test_structure_refresh",
                "scopes": ["read"]
            }
        }

        api_config = {
            "version": "v1.0",
            "domain": "structure.gmail.com",
            "api_endpoint": "https://structure.gmail.googleapis.com",
            "custom_auth_header": "Structure Bearer"
        }

        try:
            # First create a connected account
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=api_config
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)

            # Update the connected account
            updated_auth_details = {
                "oauth_token": {
                    "access_token": "updated_structure_token",
                    "refresh_token": "updated_structure_refresh",
                    "scopes": ["read", "write", "admin"]
                }
            }

            updated_api_config = {
                "version": "v2.0",
                "domain": "updated-structure.gmail.com",
                "api_endpoint": "https://updated-structure.gmail.googleapis.com",
                "custom_auth_header": "Updated Structure Bearer"
            }

            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=updated_auth_details,
                api_config=updated_api_config
            )

            # Verify response is correct type
            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)

            # Verify response has connected_account attribute
            self.assertTrue(hasattr(update_result, 'connected_account'))
            self.assertIsNotNone(update_result.connected_account)
            self.assertIsInstance(update_result.connected_account, ConnectedAccount)

            # Verify ConnectedAccount fields and types
            ca = update_result.connected_account

            # Basic string fields
            self.assertIsNotNone(ca.id)
            self.assertIsInstance(ca.id, str)
            self.assertEqual(ca.identifier, test_id)
            self.assertIsInstance(ca.identifier, str)
            self.assertIsNotNone(ca.provider)
            self.assertIsInstance(ca.provider, str)
            self.assertIsNotNone(ca.status)
            self.assertIsInstance(ca.status, str)
            self.assertIsNotNone(ca.authorization_type)
            self.assertIsInstance(ca.authorization_type, str)
            self.assertIsNotNone(ca.connector)
            self.assertIsInstance(ca.connector, str)

            # DateTime fields
            if ca.token_expires_at:
                from datetime import datetime
                self.assertIsInstance(ca.token_expires_at, datetime)
            if ca.updated_at:
                from datetime import datetime
                self.assertIsInstance(ca.updated_at, datetime)
            if ca.last_used_at:
                from datetime import datetime
                self.assertIsInstance(ca.last_used_at, datetime)

            # Dictionary fields
            self.assertIsNotNone(ca.authorization_details)
            self.assertIsInstance(ca.authorization_details, dict)

            # Verify OAuth token structure
            oauth_token = ca.authorization_details.get("oauth_token")
            self.assertIsNotNone(oauth_token)
            self.assertIsInstance(oauth_token, dict)
            self.assertEqual(oauth_token.get("access_token"), "updated_structure_token")
            self.assertEqual(oauth_token.get("refresh_token"), "updated_structure_refresh")
            self.assertEqual(oauth_token.get("scopes"), ["read", "write", "admin"])

            # API config structure verification
            self.assertIsNotNone(ca.api_config)
            self.assertIsInstance(ca.api_config, dict)

            # Verify API config content and types
            api_config_result = ca.api_config
            self.assertEqual(api_config_result["version"], "v2.0")
            self.assertIsInstance(api_config_result["version"], str)
            self.assertEqual(api_config_result["domain"], "updated-structure.gmail.com")
            self.assertIsInstance(api_config_result["domain"], str)
            self.assertEqual(api_config_result["api_endpoint"], "https://updated-structure.gmail.googleapis.com")
            self.assertIsInstance(api_config_result["api_endpoint"], str)
            self.assertEqual(api_config_result["custom_auth_header"], "Updated Structure Bearer")
            self.assertIsInstance(api_config_result["custom_auth_header"], str)

            # Verify all expected API config fields are present
            expected_api_config_fields = ["version", "domain", "custom_headers", "custom_auth_header", "api_endpoint"]
            for field in expected_api_config_fields:
                self.assertIn(field, api_config_result, f"Expected API config field '{field}' not found")

            # Test response serialization
            self.assertTrue(hasattr(update_result, 'model_dump'))
            response_dict = update_result.model_dump()
            self.assertIsInstance(response_dict, dict)
            self.assertIn('connected_account', response_dict)

            # Test ConnectedAccount serialization
            self.assertTrue(hasattr(ca, 'model_dump'))
            ca_dict = ca.model_dump()
            self.assertIsInstance(ca_dict, dict)
            self.assertIn('id', ca_dict)
            self.assertIn('identifier', ca_dict)
            self.assertIn('authorization_details', ca_dict)
            self.assertIn('api_config', ca_dict)

            # Clean up - delete the created account
            self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

        except Exception as e:
            raise e

    def test_api_config_end_to_end(self):
        """Method to test complete API config workflow: create -> get -> update -> get -> delete"""
        import uuid

        # Generate unique identifier for this test
        test_id = f"test_api_e2e_{uuid.uuid4().hex[:8]}"

        oauth_auth_details = {
            "oauth_token": {
                "access_token": "test_e2e_token",
                "refresh_token": "test_e2e_refresh",
                "scopes": ["read"]
            }
        }

        # Initial API config
        initial_api_config = {
            "version": "v1.0",
            "domain": "e2e.gmail.com",
            "api_endpoint": "https://e2e.gmail.googleapis.com",
            "custom_auth_header": "Initial E2E Bearer"
        }

        # Updated API config
        updated_api_config = {
            "version": "v2.1",
            "domain": "updated-e2e.gmail.com",
            "api_endpoint": "https://updated-e2e.gmail.googleapis.com",
            "custom_auth_header": "Updated E2E Bearer"
        }

        try:
            # Step 1: Create connected account with API config
            create_result = self.scalekit_client.actions.create_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                authorization_details=oauth_auth_details,
                api_config=initial_api_config
            )

            self.assertIsNotNone(create_result)
            self.assertIsInstance(create_result, CreateConnectedAccountResponse)
            self.assertEqual(create_result.connected_account.identifier, test_id)

            # Verify initial API config was set
            self.assertIsNotNone(create_result.connected_account.api_config)
            initial_config = create_result.connected_account.api_config
            self.assertEqual(initial_config["version"], "v1.0")
            self.assertEqual(initial_config["domain"], "e2e.gmail.com")
            self.assertEqual(initial_config["api_endpoint"], "https://e2e.gmail.googleapis.com")
            self.assertEqual(initial_config["custom_auth_header"], "Initial E2E Bearer")

            # Step 2: Get connected account and verify API config persists
            get_result = self.scalekit_client.actions.get_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(get_result)
            self.assertIsInstance(get_result, GetConnectedAccountAuthResponse)
            self.assertIsNotNone(get_result.connected_account)
            self.assertEqual(get_result.connected_account.identifier, test_id)

            # Verify API config persisted in get operation
            self.assertIsNotNone(get_result.connected_account.api_config)
            get_config = get_result.connected_account.api_config
            self.assertEqual(get_config["version"], "v1.0")
            self.assertEqual(get_config["domain"], "e2e.gmail.com")
            self.assertEqual(get_config["api_endpoint"], "https://e2e.gmail.googleapis.com")
            self.assertEqual(get_config["custom_auth_header"], "Initial E2E Bearer")

            # Step 3: Update connected account with new API config
            update_result = self.scalekit_client.actions.update_connected_account(
                connection_name="GMAIL",
                identifier=test_id,
                api_config=updated_api_config
            )

            self.assertIsNotNone(update_result)
            self.assertIsInstance(update_result, UpdateConnectedAccountResponse)
            self.assertIsNotNone(update_result.connected_account)
            self.assertEqual(update_result.connected_account.identifier, test_id)

            # Verify API config was updated
            self.assertIsNotNone(update_result.connected_account.api_config)
            updated_config = update_result.connected_account.api_config
            self.assertEqual(updated_config["version"], "v2.1")
            self.assertEqual(updated_config["domain"], "updated-e2e.gmail.com")
            self.assertEqual(updated_config["api_endpoint"], "https://updated-e2e.gmail.googleapis.com")
            self.assertEqual(updated_config["custom_auth_header"], "Updated E2E Bearer")

            # Step 4: Get connected account again and verify updates persisted
            final_get_result = self.scalekit_client.actions.get_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(final_get_result)
            self.assertIsInstance(final_get_result, GetConnectedAccountAuthResponse)
            self.assertIsNotNone(final_get_result.connected_account)
            self.assertEqual(final_get_result.connected_account.identifier, test_id)

            # Verify final API config state
            self.assertIsNotNone(final_get_result.connected_account.api_config)
            final_config = final_get_result.connected_account.api_config
            self.assertEqual(final_config["version"], "v2.1")
            self.assertEqual(final_config["domain"], "updated-e2e.gmail.com")
            self.assertEqual(final_config["api_endpoint"], "https://updated-e2e.gmail.googleapis.com")
            self.assertEqual(final_config["custom_auth_header"], "Updated E2E Bearer")

            # Verify all expected fields are present in final state
            expected_fields = ["version", "domain", "custom_headers", "custom_auth_header", "api_endpoint"]
            for field in expected_fields:
                self.assertIn(field, final_config, f"Expected field '{field}' not found in final API config")

            # Verify that all API config responses are consistent dictionaries
            for config_dict in [initial_config, get_config, updated_config, final_config]:
                self.assertIsInstance(config_dict, dict)
                for field in expected_fields:
                    self.assertIn(field, config_dict)

            # Verify the account ID remains consistent across all operations
            self.assertEqual(create_result.connected_account.id, get_result.connected_account.id)
            self.assertEqual(get_result.connected_account.id, update_result.connected_account.id)
            self.assertEqual(update_result.connected_account.id, final_get_result.connected_account.id)

            # Step 5: Clean up - delete the created account
            delete_result = self.scalekit_client.actions.delete_connected_account(
                connection_name="GMAIL",
                identifier=test_id
            )

            self.assertIsNotNone(delete_result)
            self.assertIsInstance(delete_result, DeleteConnectedAccountResponse)

        except Exception as e:
            raise e

class TestActionsMcpConfig(BaseTest):
    """Tests for MCP config operations exposed via the actions client."""

    def setUp(self):
        self.actions_client = self.scalekit_client.actions

        list_response = self.actions_client.mcp.list_configs(page_size=1)
        seed_mapping = None
        for config in list_response.configs:
            if config.connection_tool_mappings:
                seed_mapping = config.connection_tool_mappings[0]
                break

        if seed_mapping is None or not seed_mapping.tools:
            self.skipTest("No MCP config with connection mappings available for testing")

        self.seed_connection_name = seed_mapping.connection_name
        self.seed_tools = list(seed_mapping.tools)

        if not self.seed_connection_name or not self.seed_tools:
            self.skipTest("Seed MCP config missing connection name or tools")

    def test_actions_mcp_config_lifecycle(self):
        """End-to-end lifecycle: create, update, list, delete via actions client."""
        import uuid

        config_name = f"py-test-actions-config-{uuid.uuid4().hex[:8]}"
        created_config_id = None

        initial_tools = self.seed_tools[:1]
        if not initial_tools:
            self.skipTest("Seed MCP config does not contain tools for creation")

        initial_mappings = [
            McpConfigConnectionToolMapping(
                connection_name=self.seed_connection_name,
                tools=initial_tools,
            )
        ]

        try:
            create_response = self.actions_client.mcp.create_config(
                name=config_name,
                description="Test MCP config via actions client",
                connection_tool_mappings=initial_mappings,
            )
            self.assertIsInstance(create_response, CreateMcpConfigResponse)
            self.assertIsNotNone(create_response.config)
            created_config_id = create_response.config.id
            self.assertIsNotNone(created_config_id)
            self.assertEqual(create_response.config.name, config_name)

            updated_tools = self.seed_tools[:2] if len(self.seed_tools) >= 2 else list(initial_tools)
            updated_mappings = [
                McpConfigConnectionToolMapping(
                    connection_name=self.seed_connection_name,
                    tools=updated_tools,
                )
            ]

            update_response = self.actions_client.mcp.update_config(
                config_id=created_config_id,
                description="Updated MCP config via actions client",
                connection_tool_mappings=updated_mappings,
            )
            self.assertIsInstance(update_response, UpdateMcpConfigResponse)
            self.assertIsNotNone(update_response.config)
            self.assertEqual(update_response.config.id, created_config_id)
            self.assertEqual(update_response.config.name, config_name)
            self.assertTrue(update_response.config.connection_tool_mappings)
            self.assertEqual(
                update_response.config.connection_tool_mappings[0].tools,
                updated_tools,
            )

            list_response = self.actions_client.mcp.list_configs(filter_id=created_config_id)
            self.assertIsInstance(list_response, ListMcpConfigsResponse)
            self.assertTrue(
                any(cfg.id == created_config_id for cfg in list_response.configs)
            )

        finally:
            if created_config_id:
                delete_response = self.actions_client.mcp.delete_config(
                    config_id=created_config_id
                )
                self.assertIsInstance(delete_response, DeleteMcpConfigResponse)

class TestActionsMcpInstance(BaseTest):
    """Tests for MCP instance lifecycle via the actions client."""

    def setUp(self):
        self.actions_client = self.scalekit_client.actions

        configs_response = self.actions_client.mcp.list_configs(page_size=1)
        if not configs_response.configs:
            self.skipTest("No MCP configs available to create an instance")

        self.seed_config = configs_response.configs[0]
        if not self.seed_config or not self.seed_config.name:
            self.skipTest("Seed MCP config missing required name field")

    def test_actions_mcp_instance_lifecycle(self):
        """Ensure -> update -> list -> get -> auth_state -> delete."""
        import uuid

        config_name = self.seed_config.name
        user_identifier = f"py-test-instance-user-{uuid.uuid4().hex[:8]}"
        instance_name = f"py-test-instance-{uuid.uuid4().hex[:8]}"
        created_instance_id = None

        try:
            ensure_response = self.actions_client.mcp.ensure_instance(
                config_name=config_name,
                user_identifier=user_identifier,
                name=instance_name,
            )
            self.assertIsInstance(ensure_response, EnsureMcpInstanceResponse)
            self.assertIsNotNone(ensure_response.instance)
            created_instance_id = ensure_response.instance.id
            self.assertIsNotNone(created_instance_id)

            updated_name = f"{instance_name}-updated"
            update_response = self.actions_client.mcp.update_instance(
                instance_id=created_instance_id,
                name=updated_name,
            )
            self.assertIsInstance(update_response, UpdateMcpInstanceResponse)
            self.assertIsNotNone(update_response.instance)
            self.assertEqual(update_response.instance.name, updated_name)

            list_response = self.actions_client.mcp.list_instances(
                filter_id=created_instance_id
            )
            self.assertIsInstance(list_response, ListMcpInstancesResponse)
            self.assertTrue(
                any(instance.id == created_instance_id for instance in list_response.instances)
            )

            get_response = self.actions_client.mcp.get_instance(
                instance_id=created_instance_id
            )
            self.assertIsInstance(get_response, GetMcpInstanceResponse)
            self.assertIsNotNone(get_response.instance)
            self.assertEqual(get_response.instance.id, created_instance_id)

            auth_state_response = self.actions_client.mcp.get_instance_auth_state(
                instance_id=created_instance_id,
                include_auth_links=True,
            )
            self.assertIsInstance(auth_state_response, GetMcpInstanceAuthStateResponse)

        finally:
            if created_instance_id:
                delete_response = self.actions_client.mcp.delete_instance(
                    instance_id=created_instance_id
                )
                self.assertIsInstance(delete_response, DeleteMcpInstanceResponse)

    def test_actions_mcp_instance_auth_state_variants(self):
        """Verify auth state retrieval with include_auth_links toggled."""
        import uuid

        config_name = self.seed_config.name
        user_identifier = f"py-test-auth-{uuid.uuid4().hex[:8]}"
        instance_id = None

        try:
            ensure_response = self.actions_client.mcp.ensure_instance(
                config_name=config_name,
                user_identifier=user_identifier,
            )
            self.assertIsInstance(ensure_response, EnsureMcpInstanceResponse)
            self.assertIsNotNone(ensure_response.instance)

            instance_id = ensure_response.instance.id
            self.assertIsNotNone(instance_id)

            auth_state_with_links = self.actions_client.mcp.get_instance_auth_state(
                instance_id=instance_id,
                include_auth_links=True,
            )
            self.assertIsInstance(auth_state_with_links, GetMcpInstanceAuthStateResponse)
            if auth_state_with_links.connections:
                self.assertTrue(
                    any(conn.authentication_link for conn in auth_state_with_links.connections),
                    "Expected authentication links when include_auth_links is True",
                )

            auth_state_without_links = self.actions_client.mcp.get_instance_auth_state(
                instance_id=instance_id,
                include_auth_links=False,
            )
            self.assertIsInstance(auth_state_without_links, GetMcpInstanceAuthStateResponse)
            if auth_state_without_links.connections:
                self.assertTrue(
                    all(not conn.authentication_link for conn in auth_state_without_links.connections),
                    "Expected authentication links to be omitted when include_auth_links is False",
                )
        finally:
            if instance_id:
                delete_response = self.actions_client.mcp.delete_instance(
                    instance_id=instance_id
                )
                self.assertIsInstance(delete_response, DeleteMcpInstanceResponse)
