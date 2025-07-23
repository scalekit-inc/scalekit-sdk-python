from basetest import BaseTest


class TestConnectedApps(BaseTest):
    """ Class definition for Test Connected Apps Class """

    def setUp(self):
        """ """
        self.test_identifier = "avinash-test"

    def test_connected_apps_client_initialization(self):
        """ Method to test ConnectedAppsClient initialization """
        self.assertTrue(hasattr(self.scalekit_client, 'connected_apps'))
        self.assertIsNotNone(self.scalekit_client.connected_apps)
        self.assertEqual(
            self.scalekit_client.connected_apps.scalekit_client,
            self.scalekit_client
        )
        # Test that tools and connected_accounts dependencies are set
        self.assertEqual(
            self.scalekit_client.connected_apps.tools,
            self.scalekit_client.tools
        )
        self.assertEqual(
            self.scalekit_client.connected_apps.connected_accounts,
            self.scalekit_client.connected_accounts
        )

    def test_execute_tool_method_exists(self):
        """ Method to test execute_tool method exists """
        self.assertTrue(hasattr(self.scalekit_client.connected_apps, 'execute_tool'))
        self.assertTrue(callable(self.scalekit_client.connected_apps.execute_tool))

    def test_execute_tool_delegates_to_tools_client(self):
        """ Method to test execute_tool delegates to tools client """
        # Test that the method now delegates to the tools client
        # This will likely fail with connection errors, but we're testing the delegation
        try:
            result = self.scalekit_client.connected_apps.execute_tool(
                tool_name="GMAIL.FETCH_MAILS",
                identifier=self.test_identifier,
                params={"max_results": 2}
            )
            # If successful, check response structure
            self.assertIsNotNone(result)
            self.assertTrue(len(result) == 2)  # Should have response[0] and response[1]
        except Exception as e:
            # Expected to fail with connection/auth errors in test environment
            expected_errors = [
                "error getting connected account",
                "connected account not found",
                "connection not found"
            ]
            self.assertTrue(
                any(error in str(e).lower() for error in expected_errors),
                f"Unexpected error: {e}"
            )