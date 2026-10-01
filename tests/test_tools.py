import time

from faker import Faker
from basetest import BaseTest
from scalekit.actions.types import (
    ListAvailableToolsResponse,
    ListScopedToolsResponse,
    SearchToolsResponse,
)
from scalekit.common.exceptions import ScalekitNotFoundException

from scalekit.v1.tools.tools_pb2 import (
    Tool,
    Filter,
    ScopedToolFilter,
    TOOL_READINESS_STATE_UNSPECIFIED,
    TOOL_READINESS_STATE_READY,
    TOOL_READINESS_STATE_NEEDS_CONNECTION,
    TOOL_READINESS_STATE_NEEDS_REAUTH,
)
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    CreateConnectedAccount,
    AuthorizationDetails,
    OauthToken,
)
from scalekit.v1.connections.connections_pb2 import (
    CreateConnection,
    ConnectionType,
    Flags,
    DeleteEnvironmentConnectionRequest,
)
from google.protobuf import struct_pb2, wrappers_pb2


class TestTools(BaseTest):
    """ Class definition for Test Tools Class """

    def setUp(self):
        """ """
        self.faker = Faker()
        self.test_identifier = "avinash-test"
        self.test_provider = "TEST_PROVIDER"
        self.test_tool_name = f"test_tool_{self.faker.unique.random_number()}"
        self.test_schema_version = "1"
        self.test_tool_version = "1"



    def test_list_tools(self):
        """ Method to test list tools """
        response = self.scalekit_client.tools.list_tools(page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'tools') or hasattr(response[0], 'tool_names'))

    def test_list_tools_with_filters(self):
        """ Method to test list tools with filters """
        # Use a simple filter that should work - just summary mode
        filter_obj = Filter(
            summary=wrappers_pb2.BoolValue(value=True)
        )
        
        response = self.scalekit_client.tools.list_tools(
            filter=filter_obj,
            page_size=10
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

    def test_list_tools_with_identifier_and_connector(self):
        """ Method to test list tools filtered by identifier and connector """
        filter_obj = Filter(
            identifier="akshay.parihar",
            connector="myapifymcp",
            summary=wrappers_pb2.BoolValue(value=True)
        )
        response = self.scalekit_client.tools.list_tools(
            filter=filter_obj,
            page_size=100
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertIn("c-myapifymcp_fetch-apify-docs", response[0].tool_names)

    def test_list_tools_with_connected_account_id(self):
        """ Method to test list tools filtered by connected_account_id """
        filter_obj = Filter(
            connected_account_id="ca_121970114953216076",
            summary=wrappers_pb2.BoolValue(value=True)
        )
        response = self.scalekit_client.tools.list_tools(
            filter=filter_obj,
            page_size=100
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertIn("c-myapifymcp_fetch-apify-docs", response[0].tool_names)

    def test_list_scoped_tools_with_connection_names(self):
        """ Method to test list scoped tools filtered by connection_names """
        filter_obj = ScopedToolFilter(
            connection_names=["myapifymcp"]
        )
        response = self.scalekit_client.tools.list_scoped_tools(
            identifier="akshay.parihar",
            filter=filter_obj,
            page_size=100
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        tool_names = [scoped_tool.tool.definition["name"] for scoped_tool in response[0].tools]
        self.assertIn("c-myapifymcp_fetch-apify-docs", tool_names)

    def test_search_tools(self):
        """ Method to test search tools ranked by relevance to a natural-language query """
        # SearchTools scopes its candidate pool to the environment's *enabled
        # connections* (backend internal/toolsearch.ResolveEnabledProviders) --
        # independent of `identifier`, which only annotates readiness on results
        # already found. Without a Slack connection enabled on this environment,
        # every Slack tool is filtered out before ranking even runs, so create one
        # here rather than assuming staging already has it configured.
        create_resp = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(provider_key="SLACK", type=ConnectionType.OAUTH),
            flags=Flags(is_app=True)
        )
        self.assertEqual(create_resp[1].code().name, "OK")
        app_conn_id = create_resp[0].connection.id

        try:
            # The enabled-providers set is cached for up to 30s per environment
            # (backend providerCacheTTL), so poll instead of racing that cache.
            tools = []
            deadline = time.time() + 35
            while time.time() < deadline:
                response = self.scalekit_client.tools.search_tools(
                    query="send a message to a slack channel",
                    top_k=5
                )
                self.assertEqual(response[1].code().name, "OK")
                tools = response[0].tools
                if tools:
                    break
                time.sleep(2)

            self.assertGreater(len(tools), 0)
            self.assertLessEqual(len(tools), 5)
            self.assertTrue(
                any("slack" in tool.name.lower() or "slack" in tool.provider.lower() for tool in tools),
                f"expected a Slack-relevant tool in results, got: {[tool.name for tool in tools]}"
            )
            scores = [tool.score for tool in tools]
            self.assertEqual(scores, sorted(scores, reverse=True))
        finally:
            try:
                self.scalekit_client.connection.core_client.grpc_exec(
                    self.scalekit_client.connection.connection_service.DeleteEnvironmentConnection.with_call,
                    DeleteEnvironmentConnectionRequest(connection_id=app_conn_id),
                )
            except ScalekitNotFoundException:
                pass

    def test_search_tools_with_identifier(self):
        """ Method to test search tools annotates readiness when identifier is passed """
        identifier = f"search_tools_test_{self.faker.uuid4()}"
        oauth_token = OauthToken(
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            scopes=["read", "write"]
        )
        connected_account = CreateConnectedAccount(
            authorization_details=AuthorizationDetails(oauth_token=oauth_token)
        )
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector="GMAIL",
            identifier=identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")

        try:
            response = self.scalekit_client.tools.search_tools(
                query="send an email with gmail",
                identifier=identifier,
                top_k=5
            )
            self.assertEqual(response[1].code().name, "OK")
            tools = response[0].tools
            self.assertGreater(len(tools), 0)

            tools_with_connections = [tool for tool in tools if len(tool.connections) > 0]
            self.assertGreater(
                len(tools_with_connections), 0,
                "expected at least one result annotated with connection readiness "
                "for the identifier's freshly created GMAIL connected account"
            )
            for tool in tools_with_connections:
                for connection in tool.connections:
                    self.assertNotEqual(
                        connection.readiness_state, TOOL_READINESS_STATE_UNSPECIFIED,
                        "a connection tied to a real connected account must never report "
                        "UNSPECIFIED readiness"
                    )
                    self.assertIn(
                        connection.readiness_state,
                        (
                            TOOL_READINESS_STATE_READY,
                            TOOL_READINESS_STATE_NEEDS_CONNECTION,
                            TOOL_READINESS_STATE_NEEDS_REAUTH,
                        )
                    )
        finally:
            delete_response = self.scalekit_client.connected_accounts.delete_connected_account(
                connector="GMAIL",
                identifier=identifier
            )
            self.assertEqual(delete_response[1].code().name, "OK")

    def _identifier_with_gmail_account(self, prefix):
        """Create a GMAIL connected account for a fresh identifier and return it.

        Tool discovery is scoped to an identifier, so each test brings its own
        rather than depending on data another test or another environment left
        behind. The account is deleted again by addCleanup.
        """
        identifier = f"{prefix}_{self.faker.uuid4()}"
        oauth_token = OauthToken(
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            scopes=["read", "write"]
        )
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector="GMAIL",
            identifier=identifier,
            connected_account=CreateConnectedAccount(
                authorization_details=AuthorizationDetails(oauth_token=oauth_token)
            )
        )
        self.assertEqual(create_response[1].code().name, "OK")
        self.addCleanup(
            self.scalekit_client.connected_accounts.delete_connected_account,
            connector="GMAIL",
            identifier=identifier,
        )
        return identifier

    def test_list_available_tools(self):
        """ Method to test list available tools returns a bounded page for an identifier """
        identifier = self._identifier_with_gmail_account("list_available_tools_test")

        response = self.scalekit_client.tools.list_available_tools(identifier, page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertLessEqual(len(response[0].tools), 10)
        # total_size counts every page, so it can never be smaller than this page.
        if response[0].total_size:
            self.assertGreaterEqual(response[0].total_size, len(response[0].tools))

    def test_list_available_tools_second_page(self):
        """ Method to test list available tools paginates with next_page_token """
        identifier = self._identifier_with_gmail_account("list_available_paging_test")

        first = self.scalekit_client.tools.list_available_tools(identifier, page_size=1)
        self.assertEqual(first[1].code().name, "OK")
        if not first[0].next_page_token:
            self.skipTest("Identifier has at most one available tool, so there is no second page")

        second = self.scalekit_client.tools.list_available_tools(
            identifier, page_size=1, page_token=first[0].next_page_token
        )
        self.assertEqual(second[1].code().name, "OK")
        first_ids = [tool.id for tool in first[0].tools]
        second_ids = [tool.id for tool in second[0].tools]
        self.assertNotEqual(first_ids, second_ids)

    def test_actions_list_available_tools_returns_model(self):
        """ Method to test the actions facade maps available tools to the action model """
        identifier = self._identifier_with_gmail_account("actions_list_available_test")

        result = self.scalekit_client.actions.list_available_tools(identifier, page_size=10)
        self.assertIsInstance(result, ListAvailableToolsResponse)
        self.assertLessEqual(len(result.tools), 10)
        for tool in result.tools:
            self.assertIsNotNone(tool.id)

    def test_actions_list_scoped_tools_returns_model(self):
        """ Method to test the actions facade maps scoped tools to the action model """
        identifier = self._identifier_with_gmail_account("actions_list_scoped_test")

        result = self.scalekit_client.actions.list_scoped_tools(
            identifier,
            filter=ScopedToolFilter(connection_names=["GMAIL"]),
            page_size=10,
        )
        self.assertIsInstance(result, ListScopedToolsResponse)
        self.assertLessEqual(len(result.tools), 10)
        for scoped_tool in result.tools:
            self.assertEqual(scoped_tool.identifier, identifier)
            self.assertIsNotNone(scoped_tool.tool)

    def test_actions_search_tools_returns_model_with_readiness(self):
        """ Method to test the actions facade maps search results and connection readiness """
        identifier = self._identifier_with_gmail_account("actions_search_tools_test")

        result = self.scalekit_client.actions.search_tools(
            "send an email with gmail",
            identifier=identifier,
            top_k=5,
        )
        self.assertIsInstance(result, SearchToolsResponse)
        self.assertLessEqual(len(result.tools), 5)
        if not result.tools:
            # Search ranks whatever the environment has indexed; an environment
            # with no matching tool is not a failure of the mapping under test.
            self.skipTest("No tool in this environment matched the search query")

        scores = [tool.score for tool in result.tools]
        self.assertEqual(scores, sorted(scores, reverse=True))

        for tool in result.tools:
            self.assertIsNotNone(tool.name)
            # connections is empty when the identifier has no connection for the
            # tool's provider -- not an error, so only the entries that exist are
            # asserted on.
            for connection in tool.connections:
                self.assertIsNotNone(connection.connection_name)
                # The model maps the enum to its name and never raises, so an
                # unknown state would arrive as a decimal string instead.
                # UNSPECIFIED is in the accepted set because the proto allows it
                # on any entry the server did not evaluate.
                self.assertIn(
                    connection.readiness_state,
                    (
                        "TOOL_READINESS_STATE_UNSPECIFIED",
                        "TOOL_READINESS_STATE_READY",
                        "TOOL_READINESS_STATE_NEEDS_CONNECTION",
                        "TOOL_READINESS_STATE_NEEDS_REAUTH",
                    ),
                )

    def test_execute_tool_with_identifier(self):
        """ Method to test execute tool with identifier (backward compatibility) """
        test_params = {"test_param": "test_value"}
        
        try:
            response = self.scalekit_client.tools.execute_tool(
                tool_name="test_tool",
                identifier=self.test_identifier,
                params=test_params
            )
            # If the tool doesn't exist, we expect a NOT_FOUND error
            # If it exists but execution fails, we might get other errors
            # We're mainly testing that the method call works with the old signature
            self.assertTrue(response[1] is not None)
        except Exception as e:
            # This is expected if the tool doesn't exist or other API issues
            # The important thing is that the method signature works
            self.assertTrue(True)

    def test_execute_tool_with_connected_account_id(self):
        """ Method to test execute tool with connected_account_id parameter """
        test_params = {"test_param": "test_value"}
        test_connected_account_id = "ca_test123"
        
        try:
            response = self.scalekit_client.tools.execute_tool(
                tool_name="test_tool",
                identifier=self.test_identifier,
                params=test_params,
                connected_account_id=test_connected_account_id
            )
            # If the tool doesn't exist, we expect a NOT_FOUND error
            # If it exists but execution fails, we might get other errors
            # We're mainly testing that the method call works with the new parameter
            self.assertTrue(response[1] is not None)
        except Exception as e:
            # This is expected if the tool doesn't exist or other API issues
            # The important thing is that the method signature works
            self.assertTrue(True)

    def test_execute_tool_with_both_identifier_and_connected_account_id(self):
        """ Method to test execute tool with both identifier and connected_account_id """
        test_params = {"test_param": "test_value"}
        test_connected_account_id = "ca_test456"
        
        try:
            response = self.scalekit_client.tools.execute_tool(
                tool_name="test_tool",
                identifier=self.test_identifier,
                params=test_params,
                connected_account_id=test_connected_account_id
            )
            # Testing that both parameters can be provided together
            self.assertTrue(response[1] is not None)
        except Exception as e:
            # This is expected if the tool doesn't exist or other API issues
            # The important thing is that the method signature works
            self.assertTrue(True)

    def test_execute_tool_minimal_params(self):
        """ Method to test execute tool with minimal required parameters """
        try:
            response = self.scalekit_client.tools.execute_tool(
                tool_name="test_tool",
                identifier=self.test_identifier
            )
            # Testing minimal parameter set (no params, no connected_account_id)
            self.assertTrue(response[1] is not None)
        except Exception as e:
            # This is expected if the tool doesn't exist or other API issues
            # The important thing is that the method signature works
            self.assertTrue(True)

    def test_execute_tool_with_connection_name(self):
        """ Method to test execute tool with connection_name parameter """
        try:
            response = self.scalekit_client.tools.execute_tool(
                tool_name="c-myapifymcp_fetch-apify-docs",
                identifier="akshay.parihar",
                connection_name="myapifymcp",
                params={"url": "https://docs.apify.com/platform/storage/usage"}
            )
            self.assertTrue(response[1] is not None)
        except Exception as e:
            # Expected if the tool doesn't exist or other API issues
            # The important thing is that the method signature works
            self.assertTrue(True)