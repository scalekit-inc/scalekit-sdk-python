
from faker import Faker

from basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization
from scalekit.v1.clients.clients_pb2 import OrganizationClient


class TestM2MClient(BaseTest):
    """ Class definition for TestM2MClient Class """
    def setUp(self):
        self.org_id = None
        self.client_id = None

    def test_create_organization_client(self):
        """ Method to test create organization client """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )

        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0].client.client_id is not None)
        self.client_id = response[0].client.client_id
        self.assertTrue(response[0].client.secrets is not None)
        self.assertEqual(response[0].client.organization_id, self.org_id)
        self.assertEqual(response[0].client.name, m2m_client.name)
        self.assertEqual(response[0].client.description, m2m_client.description)
        self.assertEqual(response[0].client.custom_claims, m2m_client.custom_claims)
        self.assertEqual(response[0].client.scopes, m2m_client.scopes)
        self.assertEqual(response[0].client.audience, m2m_client.audience)
        self.assertEqual(response[0].client.expiry, m2m_client.expiry)

    def test_get_organization_client(self):
        """ Method to test get organization client """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.m2m_client.get_organization_client(
            organization_id=self.org_id, client_id=self.client_id
        )
        self.assertIsNotNone(create_response[0].client.client_id)
        self.assertIsNotNone(create_response[0].client.plain_secret)
        self.assertIsNone(response[0].client.plain_secret)
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].client.client_id, self.client_id)
        self.assertTrue(response[0].client.secrets, create_response[0].client.secrets)
        self.assertEqual(response[0].client.organization_id, self.org_id)
        self.assertEqual(response[0].client.name, create_response[0].client.name)
        self.assertEqual(response[0].client.description, create_response[0].client.description)
        self.assertEqual(response[0].client.custom_claims, create_response[0].client.custom_claims)
        self.assertEqual(response[0].client.scopes, create_response[0].client.scopes)
        self.assertEqual(response[0].client.audience, create_response[0].client.audience)
        self.assertEqual(response[0].client.expiry, create_response[0].client.expiry)

    def test_get_invalid_organization_client(self):
        """ Method to test get invalid organization client """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        try:
            self.scalekit_client.m2m_client.get_organization_client(
                organization_id=self.org_id, client_id=f"m2morg_{Faker().credit_card_number()}"
            )
        except Exception as exp:
            self.assertEqual(exp.args[0], "client not found")

    def test_update_organization_client(self):
        """ Method to test update organization client """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )
        self.client_id = create_response[0].client.client_id

        updated_m2m_client = OrganizationClient(
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
        )
        response = self.scalekit_client.m2m_client.update_organization_client(
            organization_id=self.org_id, client_id=self.client_id, m2m_client=updated_m2m_client
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].client.client_id, self.client_id)
        self.assertEqual(response[0].client.organization_id, self.org_id)
        self.assertEqual(response[0].client.name, m2m_client.name)
        self.assertEqual(response[0].client.description, updated_m2m_client.description)
        self.assertEqual(response[0].client.custom_claims, updated_m2m_client.custom_claims)
        self.assertEqual(response[0].client.scopes, m2m_client.scopes)
        self.assertEqual(response[0].client.audience, m2m_client.audience)
        self.assertEqual(response[0].client.expiry, m2m_client.expiry)

    def test_add_organization_client_secret(self):
        """ Method to test add organization client secret """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client)
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.m2m_client.add_organization_client_secret(
            organization_id=self.org_id, client_id=self.client_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0].plain_secret)
        self.assertIsNotNone(response[0].secret)
        new_secret_id = response[0].secret.id

        get_response = self.scalekit_client.m2m_client.get_organization_client(
            organization_id=self.org_id, client_id=self.client_id)
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertEqual(len(get_response[0].client.secrets), 2)
        self.assertEqual(get_response[0].client.secrets[1].id, new_secret_id)

    def test_remove_organization_client_secret(self):
        """ Method to test remove organization client secret """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )
        self.client_id = create_response[0].client.client_id

        secret_response = self.scalekit_client.m2m_client.add_organization_client_secret(
            organization_id=self.org_id, client_id=self.client_id
        )
        secret_id = secret_response[0].secret.id

        response = self.scalekit_client.m2m_client.remove_organization_client_secret(
            organization_id=self.org_id, client_id=self.client_id, secret_id=secret_id
        )
        self.assertEqual(response[1].code().name, "OK")

    def test_remove_last_organization_client_secret(self):
        """ Method to test remove last organization client secret """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )
        self.client_id = create_response[0].client.client_id
        secret_id = create_response[0].client.secrets[0].id

        try:
            self.scalekit_client.m2m_client.remove_organization_client_secret(
                organization_id=self.org_id, client_id=self.client_id, secret_id=secret_id
            )
        except Exception as exp:
            self.assertEqual(exp.args[0], 'last client cannot be deleted')

    def test_delete_organization_client(self):
        """ Method to test delete organization client """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )
        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )
        self.client_id = create_response[0].client.client_id

        response = self.scalekit_client.m2m_client.delete_organization_client(
            organization_id=self.org_id, client_id=self.client_id
        )
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.m2m_client.get_organization_client(
                organization_id=self.org_id, client_id=self.client_id)
        except Exception as exp:
            self.assertEqual(exp.args[0], "client not found")
            self.client_id = None

    def test_generate_token_organization_client(self):
        """ Method to test generate token organization client """
        token, client_id, client_secret  = self.__generate_token_for_org()

        self.assertIsNone(client_id)
        self.assertIsNone(client_secret)
        self.assertIsNotNone(token)

    def __generate_token_for_org(self):
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        m2m_client = OrganizationClient(
            name=Faker().company(),
            description=Faker().sentence(),
            custom_claims=[{"key": "wksp_id", "value": f"wks_{Faker().credit_card_number()}"}],
            scopes=["write", "read"],
            audience=["my-own-api"],
            expiry=3600
        )

        create_response = self.scalekit_client.m2m_client.create_organization_client(
            organization_id=self.org_id, m2m_client=m2m_client
        )

        client_id = create_response.client.client_id
        client_secret = create_response.plain_secret

        token_response = self.scalekit_client.generate_client_token(
           client_id=client_id, client_secret=client_secret
        )

        token = token_response["access_token"]
        return token, client_id, client_secret

    def test_token_validation(self):
        """ Method to test token validation """
        token, client_id, client_secret  = self.__generate_token_for_org()
        claims = self.scalekit_client.validate_access_token_and_get_claims(token=token)
        self.assertIsNotNone(claims)
        self.assertIn("client_id", claims)
        self.assertIn("my-own-api", claims["aud"])
        self.assertIn("write", claims["scopes"])
        self.assertIn("read", claims["scopes"])
        self.assertIn("wksp_id", claims["custom_claims"])


    def tearDown(self):
        # Cleanup code if needed
        if self.client_id:
            self.scalekit_client.m2m_client.delete_organization_client(organization_id=self.org_id, client_id=self.client_id)
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
