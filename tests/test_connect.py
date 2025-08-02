from basetest import BaseTest
from scalekit.connect.types import ExecuteToolResponse, MagicLinkResponse, ListConnectedAccountsResponse


class TestConnect(BaseTest):
    """Class definition for Test Connect Class"""

    def setUp(self):
        """Setup test parameters"""
        self.test_identifier = "default"
        self.test_tool_name = "GMAIL.FETCH_MAILS"

        # response = self.scalekit_client.connect.get_authorization_link(identifier = self.test_identifier, connector="GMAIL")
        # print(f"Authorization link: {response.link}")
        # input("Press Enter to continue...")




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
            # Expected to fail with connection/auth errors in test environment
            expected_errors = [
                "error getting connected account",
                "connected account not found",
                "connection not found",
                "unauthorized access"
            ]
            self.assertTrue(
                any(error in str(e).lower() for error in expected_errors),
                f"Unexpected error: {e}"
            )

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
            # Expected to fail with connection/auth errors in test environment
            expected_errors = [
                "error getting connected account",
                "connected account not found",
                "connection not found",
                "unauthorized access"
            ]
            self.assertTrue(
                any(error in str(e).lower() for error in expected_errors),
                f"Unexpected error: {e}"
            )

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

    def test_list_connected_accounts_response_structure(self):
        """Method to test ListConnectedAccountsResponse structure and methods"""
        # Test creating ListConnectedAccountsResponse directly
        response = ListConnectedAccountsResponse(
            connected_accounts=[],
            total_count=0,
            next_page_token=None,
            previous_page_token=None
        )
        
        self.assertEqual(len(response.connected_accounts), 0)
        self.assertEqual(response.total_count, 0)
        
        # Test to_dict method
        response_dict = response.to_dict()
        self.assertIsInstance(response_dict, dict)
        self.assertIn("connected_accounts", response_dict)
        self.assertIn("total_count", response_dict)

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

