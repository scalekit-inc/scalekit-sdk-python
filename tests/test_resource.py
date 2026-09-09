from basetest import BaseTest

# A real MCP server resource in the test environment. These tests assert the
# call shape and the pagination envelope, never the consent contents, so they
# hold whether or not the resource currently has consents.
TEST_RESOURCE_ID = "res_90805895235109156"


class TestResourceClient(BaseTest):
    """ Class definition for TestResourceClient Class """

    def test_list_user_consents(self):
        """ Method to test list user consents for a resource """
        response = self.scalekit_client.resources.list_user_consents(
            resource_id=TEST_RESOURCE_ID
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0].consents)
        self.assertIsInstance(response[0].total_size, int)

    def test_list_user_consents_with_page_size(self):
        """ Method to test list user consents with a page size """
        response = self.scalekit_client.resources.list_user_consents(
            resource_id=TEST_RESOURCE_ID, page_size=10
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(len(response[0].consents) <= 10)

    def test_list_user_consents_with_search(self):
        """ Method to test list user consents with a search term """
        response = self.scalekit_client.resources.list_user_consents(
            resource_id=TEST_RESOURCE_ID, search="usr_"
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0].consents)

    def test_list_user_consents_with_user_ids(self):
        """ Method to test list user consents with an exact user_ids filter """
        response = self.scalekit_client.resources.list_user_consents(
            resource_id=TEST_RESOURCE_ID, user_ids=["usr_does_not_exist"]
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(len(response[0].consents), 0)

    def test_list_user_consents_user_ids_takes_precedence_over_search(self):
        """ Method to test that user_ids is honoured alongside search """
        response = self.scalekit_client.resources.list_user_consents(
            resource_id=TEST_RESOURCE_ID, user_ids=["usr_does_not_exist"], search="usr_"
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(len(response[0].consents), 0)

    def test_list_user_consents_without_resource_id(self):
        """ Method to test list user consents without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.list_user_consents(resource_id="")

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_revoke_user_consent_without_client_id(self):
        """ Method to test revoke user consent without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.revoke_user_consent(
                client_id="", consent_id="usrcnst_1234567890"
            )

        self.assertEqual(str(context.exception), "client_id is required")

    def test_revoke_user_consent_without_consent_id(self):
        """ Method to test revoke user consent without a consent id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.revoke_user_consent(
                client_id="m2m_1234567890", consent_id=""
            )

        self.assertEqual(str(context.exception), "consent_id is required")
