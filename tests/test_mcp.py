import uuid

from faker import Faker
from basetest import BaseTest

from scalekit.v1.mcp.mcp_pb2 import (
    Mcp,
    McpConfig,
    ToolMapping,
    McpConfigConnectionToolMapping,
)


class TestMcp(BaseTest):
    """ Class definition for Test MCP Class """

    def setUp(self):
        """ """
        self.faker = Faker()
        self.test_connected_account_identifier = "default"

    def _create_test_mcp(self):
        """Helper method to create test MCP object"""
        tool_mapping = ToolMapping(
            tool_names=["gmail_fetch_mails", "gmail_search_people"],
            connection_name="GMAIL",
            status="ACTIVE"
        )

        return Mcp(
            tool_mappings=[tool_mapping],
            connected_account_identifier=self.test_connected_account_identifier,
            url="https://example.com/mcp/v1/test"
        )

    def test_create_mcp(self):
        """ Method to test create MCP """
        mcp = self._create_test_mcp()

        response = self.scalekit_client.mcp.create_mcp(mcp=mcp)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'mcp'))
        self.assertEqual(response[0].mcp.connected_account_identifier, self.test_connected_account_identifier)
        self.assertTrue(len(response[0].mcp.tool_mappings) > 0)
        self.assertEqual(response[0].mcp.tool_mappings[0].connection_name, "GMAIL")

    def test_get_mcp(self):
        """ Method to test get MCP by ID """
        # First create an MCP to get
        mcp = self._create_test_mcp()
        create_response = self.scalekit_client.mcp.create_mcp(mcp=mcp)
        self.assertEqual(create_response[1].code().name, "OK")
        created_mcp_id = create_response[0].mcp.id

        # Now get the MCP by ID
        get_response = self.scalekit_client.mcp.get_mcp(mcp_id=created_mcp_id)
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertTrue(get_response[0] is not None)
        self.assertTrue(hasattr(get_response[0], 'mcp'))
        self.assertEqual(get_response[0].mcp.id, created_mcp_id)
        self.assertEqual(get_response[0].mcp.connected_account_identifier, self.test_connected_account_identifier)

    def test_list_mcps(self):
        """ Method to test list MCPs """
        response = self.scalekit_client.mcp.list_mcps()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'mcps'))

    def test_list_mcps_with_filters(self):
        """ Method to test list MCPs with filters """
        # First create an MCP to ensure we have data to filter
        mcp = self._create_test_mcp()
        create_response = self.scalekit_client.mcp.create_mcp(mcp=mcp)
        self.assertEqual(create_response[1].code().name, "OK")

        # Test filtering by connected_account_identifier
        response = self.scalekit_client.mcp.list_mcps(
            connected_account_identifier=self.test_connected_account_identifier
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'mcps'))



        # Test filtering by both parameters
        response_with_both = self.scalekit_client.mcp.list_mcps(
            connected_account_identifier=self.test_connected_account_identifier,
        )
        self.assertEqual(response_with_both[1].code().name, "OK")
        self.assertTrue(response_with_both[0] is not None)

    def test_delete_mcp(self):
        """ Method to test delete MCP by ID """
        # First create an MCP to delete
        mcp = self._create_test_mcp()
        create_response = self.scalekit_client.mcp.create_mcp(mcp=mcp)
        self.assertEqual(create_response[1].code().name, "OK")
        created_mcp_id = create_response[0].mcp.id

        # Now delete the MCP
        delete_response = self.scalekit_client.mcp.delete_mcp(mcp_id=created_mcp_id)
        self.assertEqual(delete_response[1].code().name, "OK")
        self.assertTrue(delete_response[0] is not None)


    def _create_test_mcp_config(self):
        """Helper method to create test MCP object"""
        mcp_config = McpConfig(
            name="py-test-meeting-manager-1",
            description="Summarizes latest email and creates calendar event",
            connection_tool_mappings=[
                McpConfigConnectionToolMapping(
                    connection_name="MY_CALENDAR",
                    tools=[
                        "googlecalendar_create_event",
                        "googlecalendar_delete_event"
                    ]
                )
            ]
        )

        return mcp_config

    def test_mcp_create_update_list_delete_config(self):
        """ Method to test delete MCP Config by ID """
        # First create an MCP Config to delete
        mcp_config = self._create_test_mcp_config()
        create_response = self.scalekit_client.mcp.create_config(mcp_config=mcp_config)
        self.assertEqual(create_response[1].code().name, "OK")
        self.assertTrue(create_response[0] is not None)
        self.assertTrue(hasattr(create_response[0], 'config'))
        self.assertEqual(create_response[0].config.name, mcp_config.name)
        self.assertEqual(len(create_response[0].config.connection_tool_mappings[0].tools), 2)
        created_mcp_config_id = create_response[0].config.id

        # Now update the MCP Config
        del mcp_config.connection_tool_mappings[:]
        mcp_config.connection_tool_mappings.extend([
            McpConfigConnectionToolMapping(
                connection_name="MY_CALENDAR",
                tools=[
                    "googlecalendar_create_event",
                    "googlecalendar_delete_event",
                    "googlecalendar_list_calendars",
                ],
            )
        ])
        update_response = self.scalekit_client.mcp.update_config(
            config_id=created_mcp_config_id,
            description= "Updated description for meeting manager",
            connection_tool_mappings=mcp_config.connection_tool_mappings)
        self.assertEqual(update_response[1].code().name, "OK")
        self.assertTrue(update_response[0] is not None)
        self.assertTrue(hasattr(update_response[0], 'config'))
        self.assertEqual(update_response[0].config.name, mcp_config.name)
        self.assertEqual(len(update_response[0].config.connection_tool_mappings[0].tools), 3)

        # Now list the MCP Configs
        list_response = self.scalekit_client.mcp.list_configs()
        self.assertEqual(list_response[1].code().name, "OK")
        self.assertTrue(list_response[0] is not None)
        self.assertTrue(hasattr(list_response[0], 'configs'))

        # Now delete the MCP Config
        delete_response = self.scalekit_client.mcp.delete_config(config_id=created_mcp_config_id)
        self.assertEqual(delete_response[1].code().name, "OK")
        self.assertTrue(delete_response[0] is not None)

    def test_get_instance_auth_state_include_links_variants(self):
        """Ensure auth state retrieval works with include_auth_links True and False."""
        mcp_config = self._create_test_mcp_config()
        # Use a unique name to avoid collisions across test runs
        mcp_config.name = f"{mcp_config.name}-{uuid.uuid4().hex[:8]}"

        create_response = self.scalekit_client.mcp.create_config(mcp_config=mcp_config)
        self.assertEqual(create_response[1].code().name, "OK")
        created_config_id = create_response[0].config.id
        config_name = create_response[0].config.name

        user_identifier = f"py-test-auth-{uuid.uuid4().hex[:8]}"
        instance_name = f"py-test-instance-{uuid.uuid4().hex[:8]}"
        instance_id = None

        try:
            ensure_response = self.scalekit_client.mcp.ensure_instance(
                name=instance_name,
                config_name=config_name,
                user_identifier=user_identifier,
            )
            self.assertEqual(ensure_response[1].code().name, "OK")
            self.assertTrue(ensure_response[0] is not None)
            self.assertTrue(hasattr(ensure_response[0], 'instance'))

            instance_id = ensure_response[0].instance.id
            self.assertIsNotNone(instance_id)

            auth_state_with_links = self.scalekit_client.mcp.get_instance_auth_state(
                instance_id=instance_id,
                include_auth_links=True,
            )
            self.assertEqual(auth_state_with_links[1].code().name, "OK")
            self.assertTrue(auth_state_with_links[0] is not None)
            self.assertTrue(hasattr(auth_state_with_links[0], 'connections'))
            if auth_state_with_links[0].connections:
                self.assertTrue(
                    any(conn.authentication_link for conn in auth_state_with_links[0].connections),
                    "Expected at least one authentication link when include_auth_links is True",
                )

            auth_state_without_links = self.scalekit_client.mcp.get_instance_auth_state(
                instance_id=instance_id,
                include_auth_links=False,
            )
            self.assertEqual(auth_state_without_links[1].code().name, "OK")
            self.assertTrue(auth_state_without_links[0] is not None)
            self.assertTrue(hasattr(auth_state_without_links[0], 'connections'))
            if auth_state_without_links[0].connections:
                self.assertTrue(
                    all(not conn.authentication_link for conn in auth_state_without_links[0].connections),
                    "Expected authentication links to be omitted when include_auth_links is False",
                )
        finally:
            if instance_id:
                self.scalekit_client.mcp.delete_instance(instance_id=instance_id)
            self.scalekit_client.mcp.delete_config(config_id=created_config_id)
