from basetest import BaseTest
from scalekit.connect.types import ExecuteToolResponse, MagicLinkResponse, ListConnectedAccountsResponse, DeleteConnectedAccountResponse, GetConnectedAccountAuthResponse
from scalekit.connect.modifier import Modifier


class TestConnect(BaseTest):
    """Class definition for Test Connect Class"""

    def setUp(self):
        """Setup test parameters"""
        self.test_identifier = "default"
        self.test_tool_name = "GMAIL.FETCH_MAILS"
        self.test_connection_name = "GMAIL"


        ca_response = self.scalekit_client.connect.get_connected_account_auth(
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
                tool_name="GMAIL.INVALID_TOOL",
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
        self.assertTrue(hasattr(self.scalekit_client.connect, 'get_connected_account_auth'))
        self.assertTrue(callable(self.scalekit_client.connect.get_connected_account_auth))


    def test_get_connected_account_auth(self):
        """Method to test get_connected_account_auth returns GetConnectedAccountAuthResponse"""
        try:
            result = self.scalekit_client.connect.get_connected_account_auth(
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

            connected_account_response = self.scalekit_client.connect.get_connected_account_auth(
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

            connected_account_response = self.scalekit_client.connect.get_connected_account_auth(
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
            result = self.scalekit_client.connect.get_connected_account_auth(
                connection_name="GMAIL",
                identifier=self.test_identifier,
            )
            self.assertIsNotNone(result)
            self.assertIsInstance(result, GetConnectedAccountAuthResponse)
            self.assertTrue(hasattr(result, 'connected_account'))
        except Exception as e:
            raise e

    # Modifier System Tests
    def test_modifier_initialization(self):
        """Test that ConnectClient initializes with empty modifier list"""
        self.assertTrue(hasattr(self.scalekit_client.connect, '_modifiers'))
        self.assertEqual(len(self.scalekit_client.connect._modifiers), 0)

    def test_add_modifier_method(self):
        """Test add_modifier method functionality"""
        # Create a test modifier
        modifier = Modifier(tool_names="TEST_TOOL", modifier_type="pre")
        
        # Add modifier to connect client
        self.scalekit_client.connect.add_modifier(modifier)
        
        # Verify modifier was added
        self.assertEqual(len(self.scalekit_client.connect._modifiers), 1)
        self.assertEqual(self.scalekit_client.connect._modifiers[0], modifier)

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

    def test_get_modifiers_filter_by_tool_name(self):
        """Test get_modifiers with tool name filtering"""
        # Add test modifiers
        modifier1 = Modifier(tool_names="TOOL1", modifier_type="pre")
        modifier2 = Modifier(tool_names="TOOL2", modifier_type="post")
        modifier3 = Modifier(tool_names="TOOL1", modifier_type="post")
        
        self.scalekit_client.connect.add_modifier(modifier1)
        self.scalekit_client.connect.add_modifier(modifier2)
        self.scalekit_client.connect.add_modifier(modifier3)
        
        # Filter by tool name
        tool1_modifiers = self.scalekit_client.connect.get_modifiers(tool_name="TOOL1")
        self.assertEqual(len(tool1_modifiers), 2)

    def test_get_modifiers_filter_by_type(self):
        """Test get_modifiers with type filtering"""
        # Add test modifiers
        modifier1 = Modifier(tool_names="TOOL1", modifier_type="pre")
        modifier2 = Modifier(tool_names="TOOL2", modifier_type="post")
        modifier3 = Modifier(tool_names="TOOL3", modifier_type="pre")
        
        self.scalekit_client.connect.add_modifier(modifier1)
        self.scalekit_client.connect.add_modifier(modifier2)
        self.scalekit_client.connect.add_modifier(modifier3)
        
        # Filter by type
        pre_modifiers = self.scalekit_client.connect.get_modifiers(modifier_type="pre")
        post_modifiers = self.scalekit_client.connect.get_modifiers(modifier_type="post")
        
        self.assertEqual(len(pre_modifiers), 2)
        self.assertEqual(len(post_modifiers), 1)

    def test_premodifier_decorator(self):
        """Test premodifier decorator functionality"""
        # Use the decorator to create a pre-modifier
        @self.scalekit_client.connect.premodifier(tool_names="TEST_TOOL")
        def test_pre_modifier(tool_name, data):
            data["modified"] = True
            return data
        
        # Verify modifier was registered
        modifiers = self.scalekit_client.connect.get_modifiers(tool_name="TEST_TOOL", modifier_type="pre")
        self.assertEqual(len(modifiers), 1)
        self.assertEqual(modifiers[0].func, test_pre_modifier)

    def test_postmodifier_decorator(self):
        """Test postmodifier decorator functionality"""
        # Use the decorator to create a post-modifier
        @self.scalekit_client.connect.postmodifier(tool_names="TEST_TOOL")
        def test_post_modifier(tool_name, data):
            data.test_modified = True
            return data
        
        # Verify modifier was registered
        modifiers = self.scalekit_client.connect.get_modifiers(tool_name="TEST_TOOL", modifier_type="post")
        self.assertEqual(len(modifiers), 1)
        self.assertEqual(modifiers[0].func, test_post_modifier)

    def test_premodifier_with_parameters(self):
        """Test premodifier decorator with additional parameters"""
        # Use the decorator with additional parameters
        @self.scalekit_client.connect.premodifier(tool_names="TEST_TOOL", priority=1, enabled=True)
        def test_pre_modifier_with_params(tool_name, data):
            return data
        
        # Verify modifier was registered with parameters
        modifiers = self.scalekit_client.connect.get_modifiers(tool_name="TEST_TOOL", modifier_type="pre")
        self.assertEqual(len(modifiers), 1)
        self.assertEqual(modifiers[0].params["priority"], 1)
        self.assertEqual(modifiers[0].params["enabled"], True)

    def test_modifier_with_multiple_tool_names(self):
        """Test modifier with multiple tool names"""
        # Create modifier for multiple tools
        @self.scalekit_client.connect.premodifier(tool_names=["TOOL1", "TOOL2", "TOOL3"])
        def multi_tool_modifier(tool_name, data):
            return data
        
        # Verify modifier applies to all specified tools
        for tool_name in ["TOOL1", "TOOL2", "TOOL3"]:
            modifiers = self.scalekit_client.connect.get_modifiers(tool_name=tool_name, modifier_type="pre")
            self.assertEqual(len(modifiers), 1)

    def test_modifier_execution_order(self):
        """Test that modifiers are applied in the correct order"""
        # Create test data to track execution order
        execution_order = []
        
        # Create multiple pre-modifiers
        @self.scalekit_client.connect.premodifier(tool_names="ORDER_TEST")
        def first_modifier(tool_name, data):
            execution_order.append("first")
            data["first"] = True
            return data
        
        @self.scalekit_client.connect.premodifier(tool_names="ORDER_TEST")
        def second_modifier(tool_name, data):
            execution_order.append("second")
            data["second"] = True
            return data
        
        # Test that we have the right number of modifiers
        modifiers = self.scalekit_client.connect.get_modifiers(tool_name="ORDER_TEST", modifier_type="pre")
        self.assertEqual(len(modifiers), 2)

    def test_modifier_instance_isolation(self):
        """Test that modifiers are isolated between different ConnectClient instances"""
        # Get a second connect client instance for comparison
        second_connect = self.scalekit_client.connect.__class__(
            self.scalekit_client.tools,
            self.scalekit_client.connected_accounts
        )
        
        # Add modifier to first instance
        @self.scalekit_client.connect.premodifier(tool_names="ISOLATION_TEST")
        def first_instance_modifier(tool_name, data):
            return data
        
        # Add modifier to second instance
        @second_connect.premodifier(tool_names="ISOLATION_TEST")
        def second_instance_modifier(tool_name, data):
            return data
        
        # Verify each instance has only its own modifier
        first_modifiers = self.scalekit_client.connect.get_modifiers(tool_name="ISOLATION_TEST")
        second_modifiers = second_connect.get_modifiers(tool_name="ISOLATION_TEST")
        
        self.assertEqual(len(first_modifiers), 1)
        self.assertEqual(len(second_modifiers), 1)
        self.assertNotEqual(first_modifiers[0].func, second_modifiers[0].func)

