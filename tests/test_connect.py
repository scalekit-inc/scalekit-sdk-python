from basetest import BaseTest
from scalekit.tool_request import ToolRequest
from scalekit.execute_tool_response import ExecuteToolResponse


class TestConnect(BaseTest):
    """Class definition for Test Connect Class"""

    def setUp(self):
        """Setup test parameters"""
        self.test_identifier = "avinash.kamath@scalekit.com"
        self.test_tool_name = "SLACK.SEND_MESSAGE"


    def test_execute_tool_with_slack_send_message(self):
        """Method to test execute_tool with SLACK.SEND_MESSAGE"""
        input_data = {
            "channel": "#connect",
            "text": "Hello from Scalekit SDK test!",
            "username": "Scalekit Bot"
        }
        
        try:
            result = self.scalekit_client.connect.execute_tool(
                input_data=input_data,
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

