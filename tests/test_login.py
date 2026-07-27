import os

from basetest import BaseTest


class TestLogin(BaseTest):
    """ Class definition for Test Login Class """

    def test_update_login_user_details_invalid_user_type(self):
        """ Client-side validation: a non-mapping user raises TypeError (always runs) """
        with self.assertRaises(TypeError):
            self.scalekit_client.auth.update_login_user_details(
                connection_id="conn_test",
                login_request_id="req_test",
                user=12345,
            )

    def test_update_login_user_details(self):
        """ Live test: update login user details and read back auth_request_id """
        connection_id = os.environ.get("SCALEKIT_TEST_CONNECTION_ID")
        login_request_id = os.environ.get("SCALEKIT_TEST_LOGIN_REQUEST_ID")
        if not connection_id or not login_request_id:
            self.skipTest(
                "SCALEKIT_TEST_CONNECTION_ID / SCALEKIT_TEST_LOGIN_REQUEST_ID not set"
            )

        response = self.scalekit_client.auth.update_login_user_details(
            connection_id=connection_id,
            login_request_id=login_request_id,
            user={"email": "test@example.com"},
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(response[0].auth_request_id)
