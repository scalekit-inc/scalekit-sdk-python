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
