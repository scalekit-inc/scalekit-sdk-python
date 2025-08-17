from faker import Faker
from basetest import BaseTest

from scalekit.v1.mcp.mcp_pb2 import (
    Mcp,
    ToolMapping,
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