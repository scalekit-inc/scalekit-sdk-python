from basetest import BaseTest
from scalekit.connect.types import ExecuteToolResponse, MagicLinkResponse, ListConnectedAccountsResponse, DeleteConnectedAccountResponse, GetConnectedAccountAuthResponse, ToolMapping
from scalekit.connect.modifier import Modifier


class TestConnect(BaseTest):
    """Class definition for Test Connect Class"""

    def setUp(self):
        """Setup test parameters"""
        self.test_identifier = "default"
        self.test_tool_name = "gmail_fetch_mails"
        self.test_connection_name = "GMAIL"


        ca_response = self.scalekit_client.connect.get_connected_account(
            connection_name=self.test_connection_name,
            identifier=self.test_identifier
        )

        self.test_connected_account_id = ca_response.connected_account.id
        if ca_response.connected_account.status != "ACTIVE":
            response = self.scalekit_client.connect.get_authorization_link(identifier = self.test_identifier, connector="GMAIL")
            print(f"Authorization link: {response.link}")
            input("Press Enter to continue...")




    def test_execute_tool(self):
        """Method to test execute_tool with SLACK.SEND_MESSAGE"""
        tool_input = {
            "max_results": 1,
        }

        try:
            result = self.scalekit_client.connect.execute_tool(
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
        """Method to test get_connected_account_auth returns GetConnectedAccountAuthResponse"""
        try:
            result = self.scalekit_client.connect.get_connected_account(
                connection_name="GMAIL",
                identifier=self.test_identifier
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, GetConnectedAccountAuthResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
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


    def test_create_mcp_method_exists(self):
        """Method to test create_mcp method exists"""
        self.assertTrue(hasattr(self.scalekit_client.connect, 'create_mcp'))
        self.assertTrue(callable(self.scalekit_client.connect.create_mcp))

    def test_create_mcp_success(self):
        """Method to test create_mcp creates MCP server successfully"""
        import uuid
        from scalekit.connect.types import CreateMcpResponse
        
        # Generate unique identifier for this test
        test_identifier = 'default'
        
        # Define test MCP configuration
        tool_mappings = [
            ToolMapping(
                tool_names=["gmail_fetch_mails", "gmail_send_mails"],
                connection_name="GMAIL",
            )
        ]
        
        try:
            # Create MCP server
            result = self.scalekit_client.connect.create_mcp(
                identifier=test_identifier,
                tool_mappings=tool_mappings,
            )
            
            # Verify response structure
            self.assertIsNotNone(result)
            self.assertIsInstance(result, CreateMcpResponse)
            self.assertTrue(hasattr(result, 'id'))
            self.assertTrue(hasattr(result, 'identifier'))
            self.assertTrue(hasattr(result, 'url'))
            print(result.url)
            
            # Verify the created MCP has expected values
            self.assertIsNotNone(result.id)
            
        except Exception as e:
            raise e

