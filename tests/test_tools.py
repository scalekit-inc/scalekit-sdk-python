from faker import Faker
from basetest import BaseTest

from scalekit.v1.tools.tools_pb2 import (
    Tool,
    Filter
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
        response = self.scalekit_client.tools.list_tools()
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