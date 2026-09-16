from faker import Faker

from basetest import BaseTest
from scalekit.common.exceptions import ScalekitBadRequestException, ScalekitNotFoundException
from scalekit.v1.clients.clients_pb2 import ResourceClient as ResourceClientProto
from scalekit.v1.clients.clients_pb2 import ResourceType

# A real MCP server resource in the test environment. These tests assert the
# call shape and the pagination envelope, never the consent contents, so they
# hold whether or not the resource currently has consents.
TEST_RESOURCE_ID = "res_90805895235109156"

# Syntactically valid but nonexistent resource id, used to assert that
# delete_resource_client refuses to touch a client under the wrong resource
# scope instead of trusting the id pair blindly.
OTHER_RESOURCE_ID = "res_999999999999999999"


class TestResource(BaseTest):
    """ Class definition for TestResource Class """

    def test_get_resource(self):
        """ Method to test get resource by id, including its allowed scopes """
        response = self.scalekit_client.resources.get_resource(
            resource_id=TEST_RESOURCE_ID
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].resource.id, TEST_RESOURCE_ID)
        self.assertIsNotNone(response[0].resource.scopes)

    def test_get_resource_without_resource_id(self):
        """ Method to test get resource without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.get_resource(resource_id="")

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_get_resource_nonexistent(self):
        """ Method to test get resource for a nonexistent resource id """
        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.resources.get_resource(resource_id=OTHER_RESOURCE_ID)

    def test_list_resources(self):
        """ Method to test list resources of a given type in the environment """
        response = self.scalekit_client.resources.list_resources(
            resource_type=ResourceType.MCP_SERVER
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertIsInstance(response[0].total_size, int)
        response_resource_ids = [r.id for r in response[0].resources]
        self.assertIn(TEST_RESOURCE_ID, response_resource_ids)

    def test_list_resources_with_page_size(self):
        """ Method to test list resources with a page size """
        response = self.scalekit_client.resources.list_resources(
            resource_type=ResourceType.MCP_SERVER, page_size=1
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(len(response[0].resources) <= 1)

    def test_list_resources_without_resource_type(self):
        """ Method to test list resources without a resource type """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.list_resources(resource_type=None)

        self.assertEqual(str(context.exception), "resource_type is required")


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


class TestResourceClientCRUD(BaseTest):
    """ Class definition for TestResourceClientCRUD Class """

    def setUp(self):
        self.client_id = None

    def tearDown(self):
        if self.client_id:
            try:
                self.scalekit_client.resources.delete_resource_client(
                    resource_id=TEST_RESOURCE_ID, client_id=self.client_id
                )
            except ScalekitNotFoundException:
                pass  # The test already deleted the client

    def test_create_resource_client(self):
        """ Method to test create resource client """
        client = ResourceClientProto(
            name=Faker().company(),
            description=Faker().sentence(),
            scopes=["read", "write"],
        )
        response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=client
        )
        self.client_id = response[0].client.client_id

        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0].client.client_id)
        self.assertIsNotNone(response[0].plain_secret)
        self.assertEqual(response[0].client.resource_id, TEST_RESOURCE_ID)
        self.assertEqual(response[0].client.name, client.name)
        self.assertEqual(response[0].client.description, client.description)
        self.assertEqual(list(response[0].client.scopes), ["read", "write"])

    def test_create_resource_client_without_resource_id(self):
        """ Method to test create resource client without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.create_resource_client(
                resource_id="", client=ResourceClientProto(name="x")
            )

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_get_resource_client(self):
        """ Method to test get resource client """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.resources.get_resource_client(
            resource_id=TEST_RESOURCE_ID, client_id=self.client_id
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].client.client_id, self.client_id)
        self.assertIsNotNone(response[0].consented_users)

    def test_get_resource_client_without_resource_id(self):
        """ Method to test get resource client without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.get_resource_client(resource_id="", client_id="m2m_1234567890")

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_get_resource_client_without_client_id(self):
        """ Method to test get resource client without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.get_resource_client(resource_id=TEST_RESOURCE_ID, client_id="")

        self.assertEqual(str(context.exception), "client_id is required")

    def test_list_resource_clients(self):
        """ Method to test list resource clients """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.resources.list_resource_clients(resource_id=TEST_RESOURCE_ID)
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsInstance(response[0].total_dcr_clients, int)
        self.assertIsInstance(response[0].total_static_clients, int)
        response_client_ids = [c.client_id for c in response[0].clients]
        self.assertIn(self.client_id, response_client_ids)

    def test_list_resource_clients_without_resource_id(self):
        """ Method to test list resource clients without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.list_resource_clients(resource_id="")

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_update_resource_client(self):
        """ Method to test update resource client """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name="Original Name")
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.resources.update_resource_client(
            resource_id=TEST_RESOURCE_ID,
            client_id=self.client_id,
            client=ResourceClientProto(name="Updated Name", description="Updated description"),
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].client.name, "Updated Name")
        self.assertEqual(response[0].client.description, "Updated description")

    def test_update_resource_client_scopes_via_update_mask(self):
        """ Method to test update resource client scopes using the update mask """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company(), scopes=["read"])
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.resources.update_resource_client(
            resource_id=TEST_RESOURCE_ID,
            client_id=self.client_id,
            client=ResourceClientProto(scopes=["read", "write"]),
            update_mask=["scopes"],
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(list(response[0].client.scopes), ["read", "write"])

    def test_update_resource_client_without_resource_id(self):
        """ Method to test update resource client without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.update_resource_client(
                resource_id="", client_id="m2m_1234567890", client=ResourceClientProto()
            )

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_update_resource_client_without_client_id(self):
        """ Method to test update resource client without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.update_resource_client(
                resource_id=TEST_RESOURCE_ID, client_id="", client=ResourceClientProto()
            )

        self.assertEqual(str(context.exception), "client_id is required")

    def test_update_resource_client_rejects_audience_in_update_mask(self):
        """ Method to test that update rejects an audience path in update_mask, since it can never take effect """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.update_resource_client(
                resource_id=TEST_RESOURCE_ID,
                client_id="m2m_1234567890",
                client=ResourceClientProto(audience=["https://api.example.com"]),
                update_mask=["audience"],
            )

        self.assertEqual(str(context.exception), "audience cannot be changed via update; it is fixed at creation")

    def test_delete_resource_client(self):
        """ Method to test delete resource client """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        client_id = create_response[0].client.client_id

        response = self.scalekit_client.resources.delete_resource_client(
            resource_id=TEST_RESOURCE_ID, client_id=client_id
        )
        self.assertEqual(response[1].code().name, "OK")

        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.resources.get_resource_client(
                resource_id=TEST_RESOURCE_ID, client_id=client_id
            )

    def test_delete_resource_client_without_resource_id(self):
        """ Method to test delete resource client without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.delete_resource_client(resource_id="", client_id="m2m_1234567890")

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_delete_resource_client_without_client_id(self):
        """ Method to test delete resource client without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.delete_resource_client(resource_id=TEST_RESOURCE_ID, client_id="")

        self.assertEqual(str(context.exception), "client_id is required")

    def test_delete_resource_client_refuses_wrong_resource(self):
        """ Method to test that delete refuses a client that does not belong to the given resource """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        # OTHER_RESOURCE_ID doesn't exist, so the client can't belong to it —
        # the server's own resource-scoping on GetResourceClient refuses the
        # delete before it ever runs, and the SDK-side ownership check in
        # delete_resource_client is the second line of defense for a backend
        # that didn't enforce this.
        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.resources.delete_resource_client(
                resource_id=OTHER_RESOURCE_ID, client_id=self.client_id
            )

        # The client must still exist under its real resource.
        still_there = self.scalekit_client.resources.get_resource_client(
            resource_id=TEST_RESOURCE_ID, client_id=self.client_id
        )
        self.assertEqual(still_there[0].client.client_id, self.client_id)


class TestResourceClientSecret(BaseTest):
    """ Class definition for TestResourceClientSecret Class """

    def setUp(self):
        self.client_id = None

    def tearDown(self):
        if self.client_id:
            try:
                self.scalekit_client.resources.delete_resource_client(
                    resource_id=TEST_RESOURCE_ID, client_id=self.client_id
                )
            except ScalekitNotFoundException:
                pass  # The test already deleted the client

    def test_create_and_delete_resource_client_secret(self):
        """ Method to test create then delete a secret for a resource client """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        secret_response = self.scalekit_client.resources.create_resource_client_secret(
            resource_id=TEST_RESOURCE_ID, client_id=self.client_id
        )
        self.assertEqual(secret_response[1].code().name, "OK")
        self.assertTrue(secret_response[0].plain_secret)
        self.assertTrue(secret_response[0].secret.id)

        delete_response = self.scalekit_client.resources.delete_resource_client_secret(
            resource_id=TEST_RESOURCE_ID,
            client_id=self.client_id,
            secret_id=secret_response[0].secret.id,
        )
        self.assertEqual(delete_response[1].code().name, "OK")

    def test_create_resource_client_secret_refuses_wrong_resource(self):
        """ Method to test that create secret refuses a client that does not belong to the given resource """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.resources.create_resource_client_secret(
                resource_id=OTHER_RESOURCE_ID, client_id=self.client_id
            )

    def test_delete_resource_client_secret_refuses_wrong_resource(self):
        """ Method to test that delete secret refuses a client that does not belong to the given resource """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        secret_response = self.scalekit_client.resources.create_resource_client_secret(
            resource_id=TEST_RESOURCE_ID, client_id=self.client_id
        )

        with self.assertRaises(ScalekitNotFoundException):
            self.scalekit_client.resources.delete_resource_client_secret(
                resource_id=OTHER_RESOURCE_ID,
                client_id=self.client_id,
                secret_id=secret_response[0].secret.id,
            )

    def test_create_resource_client_secret_without_resource_id(self):
        """ Method to test create resource client secret without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.create_resource_client_secret(
                resource_id="", client_id="m2m_1234567890"
            )

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_create_resource_client_secret_without_client_id(self):
        """ Method to test create resource client secret without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.create_resource_client_secret(
                resource_id=TEST_RESOURCE_ID, client_id=""
            )

        self.assertEqual(str(context.exception), "client_id is required")

    def test_delete_resource_client_secret_without_resource_id(self):
        """ Method to test delete resource client secret without a resource id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.delete_resource_client_secret(
                resource_id="", client_id="m2m_1234567890", secret_id="ksec_1234567890"
            )

        self.assertEqual(str(context.exception), "resource_id is required")

    def test_delete_resource_client_secret_without_client_id(self):
        """ Method to test delete resource client secret without a client id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.delete_resource_client_secret(
                resource_id=TEST_RESOURCE_ID, client_id="", secret_id="ksec_1234567890"
            )

        self.assertEqual(str(context.exception), "client_id is required")

    def test_delete_resource_client_secret_without_secret_id(self):
        """ Method to test delete resource client secret without a secret id """
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.resources.delete_resource_client_secret(
                resource_id=TEST_RESOURCE_ID, client_id="m2m_1234567890", secret_id=""
            )

        self.assertEqual(str(context.exception), "secret_id is required")

    def test_delete_resource_client_secret_refuses_when_last_remaining(self):
        """ Method to test that delete secret refuses to remove a client's only remaining secret """
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        fetched = self.scalekit_client.resources.get_resource_client(
            resource_id=TEST_RESOURCE_ID, client_id=self.client_id
        )
        only_secret_id = fetched[0].client.secrets[0].id

        with self.assertRaises(ScalekitBadRequestException):
            self.scalekit_client.resources.delete_resource_client_secret(
                resource_id=TEST_RESOURCE_ID,
                client_id=self.client_id,
                secret_id=only_secret_id,
            )

    def test_create_resource_client_secret_refuses_past_limit(self):
        """ Method to test that creating a secret past the server-enforced per-client limit fails """
        # The exact limit is environment-configurable (verified live: 5 in
        # Scalekit's own dev environment, not the dashboard's stricter
        # UI-only threshold of 2) — probe until the server actually refuses
        # rather than asserting a specific count.
        create_response = self.scalekit_client.resources.create_resource_client(
            resource_id=TEST_RESOURCE_ID, client=ResourceClientProto(name=Faker().company())
        )
        self.client_id = create_response[0].client.client_id

        limit_hit = False
        for _ in range(20):
            try:
                self.scalekit_client.resources.create_resource_client_secret(
                    resource_id=TEST_RESOURCE_ID, client_id=self.client_id
                )
            except ScalekitBadRequestException:
                limit_hit = True
                break

        self.assertTrue(limit_hit)
