from faker import Faker
from basetest import BaseTest

from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    CreateConnectedAccount,
    UpdateConnectedAccount,
    AuthorizationDetails,
    OauthToken,
)
from google.protobuf import struct_pb2


class TestConnectedAccounts(BaseTest):
    """ Class definition for Test Connected Accounts Class """

    def setUp(self):
        """ """
        self.faker = Faker()
        self.test_connector = "GMAIL"
        self.test_identifier = f"test_app_{self.faker.unique.random_number()}"

    def _create_oauth_connected_account(self):
        """Helper method to create OAuth connected account"""
        oauth_token = OauthToken(
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            scopes=["read", "write"]
        )
        auth_details = AuthorizationDetails(oauth_token=oauth_token)
        return CreateConnectedAccount(authorization_details=auth_details)

    def test_list_connected_accounts(self):
        """ Method to test list connected accounts """
        response = self.scalekit_client.connected_accounts.list_connected_accounts()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'connected_accounts'))
        self.assertTrue(hasattr(response[0], 'total_size'))

    def test_list_connected_accounts_with_filters(self):
        """ Method to test list connected accounts with filters """
        response = self.scalekit_client.connected_accounts.list_connected_accounts(
            connector=self.test_connector,
            page_size=10
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

    def test_create_connected_account_with_oauth(self):
        """ Method to test create connected account with OAuth """
        connected_account = self._create_oauth_connected_account()
        
        response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=self.test_identifier,
            connected_account=connected_account
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'connected_account'))
        self.assertEqual(response[0].connected_account.identifier, self.test_identifier)

    def test_create_connected_account_with_static_auth(self):
        """ Method to test create connected account with static auth (skipped for OAUTH-only connector) """
        # TEST-123 connector only supports OAuth, so we'll create another OAuth test instead
        connected_account = self._create_oauth_connected_account()
        
        static_identifier = f"static_{self.test_identifier}"
        response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=static_identifier,
            connected_account=connected_account
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'connected_account'))
        self.assertEqual(response[0].connected_account.identifier, static_identifier)

    def test_get_connected_account_by_identifier(self):
        """ Method to test get connected account by identifier """
        connected_account = self._create_oauth_connected_account()
        get_identifier = f"get_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=get_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        
        # Now get it by identifier
        get_response = self.scalekit_client.connected_accounts.get_connected_account_by_identifier(
            connector=self.test_connector,
            identifier=get_identifier
        )
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertTrue(get_response[0] is not None)
        self.assertTrue(hasattr(get_response[0], 'connected_account'))
        self.assertEqual(get_response[0].connected_account.identifier, get_identifier)

    def test_update_connected_account(self):
        """ Method to test update connected account """
        connected_account = self._create_oauth_connected_account()
        update_identifier = f"update_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=update_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        
        # Now update it
        updated_oauth_token = OauthToken(
            access_token="updated_access_token",
            refresh_token="updated_refresh_token",
            scopes=["read", "write", "admin"]
        )
        updated_auth_details = AuthorizationDetails(oauth_token=updated_oauth_token)
        
        update_connected_account = UpdateConnectedAccount(
            authorization_details=updated_auth_details
        )
        
        update_response = self.scalekit_client.connected_accounts.update_connected_account(
            connector=self.test_connector,
            identifier=update_identifier,
            connected_account=update_connected_account
        )
        self.assertEqual(update_response[1].code().name, "OK")
        self.assertTrue(update_response[0] is not None)
        self.assertTrue(hasattr(update_response[0], 'connected_account'))
        self.assertEqual(update_response[0].connected_account.identifier, update_identifier)

    def test_get_magic_link_for_connected_account(self):
        """ Method to test get magic link for connected account """
        connected_account = self._create_oauth_connected_account()
        magic_link_identifier = f"magic_link_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=magic_link_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        
        # Now get magic link
        magic_link_response = self.scalekit_client.connected_accounts.get_magic_link_for_connected_account(
            connector=self.test_connector,
            identifier=magic_link_identifier
        )
        self.assertEqual(magic_link_response[1].code().name, "OK")
        self.assertTrue(magic_link_response[0] is not None)
        self.assertTrue(hasattr(magic_link_response[0], 'link'))
        self.assertTrue(hasattr(magic_link_response[0], 'expiry'))

    def test_delete_connected_account(self):
        """ Method to test delete connected account """
        connected_account = self._create_oauth_connected_account()
        delete_identifier = f"delete_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=delete_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        
        # Now delete it
        delete_response = self.scalekit_client.connected_accounts.delete_connected_account(
            connector=self.test_connector,
            identifier=delete_identifier
        )
        self.assertEqual(delete_response[1].code().name, "OK")
        self.assertTrue(delete_response[0] is not None)

    def test_update_connected_account_with_connected_account_id(self):
        """ Method to test update connected account with connected_account_id parameter """
        connected_account = self._create_oauth_connected_account()
        update_identifier = f"update_with_id_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=update_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        created_account_id = create_response[0].connected_account.id
        
        # Now update it using connected_account_id
        updated_oauth_token = OauthToken(
            access_token="updated_with_id_access_token",
            refresh_token="updated_with_id_refresh_token",
            scopes=["read", "write", "admin"]
        )
        updated_auth_details = AuthorizationDetails(oauth_token=updated_oauth_token)
        
        update_connected_account = UpdateConnectedAccount(
            authorization_details=updated_auth_details
        )
        
        update_response = self.scalekit_client.connected_accounts.update_connected_account(
            connector=self.test_connector,
            identifier=update_identifier,
            connected_account=update_connected_account,
            connected_account_id=created_account_id
        )
        self.assertEqual(update_response[1].code().name, "OK")
        self.assertTrue(update_response[0] is not None)
        self.assertTrue(hasattr(update_response[0], 'connected_account'))
        self.assertEqual(update_response[0].connected_account.id, created_account_id)

    def test_get_connected_account_by_identifier_with_connected_account_id(self):
        """ Method to test get connected account by identifier with connected_account_id parameter """
        connected_account = self._create_oauth_connected_account()
        get_identifier = f"get_with_id_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=get_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        created_account_id = create_response[0].connected_account.id
        
        # Now get it by identifier with connected_account_id
        get_response = self.scalekit_client.connected_accounts.get_connected_account_by_identifier(
            connector=self.test_connector,
            identifier=get_identifier,
            connected_account_id=created_account_id
        )
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertTrue(get_response[0] is not None)
        self.assertTrue(hasattr(get_response[0], 'connected_account'))
        self.assertEqual(get_response[0].connected_account.id, created_account_id)
        self.assertEqual(get_response[0].connected_account.identifier, get_identifier)

    def test_get_magic_link_for_connected_account_with_connected_account_id(self):
        """ Method to test get magic link for connected account with connected_account_id parameter """
        connected_account = self._create_oauth_connected_account()
        magic_link_identifier = f"magic_link_with_id_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=magic_link_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        created_account_id = create_response[0].connected_account.id
        
        # Now get magic link with connected_account_id
        magic_link_response = self.scalekit_client.connected_accounts.get_magic_link_for_connected_account(
            connector=self.test_connector,
            identifier=magic_link_identifier,
            connected_account_id=created_account_id
        )
        self.assertEqual(magic_link_response[1].code().name, "OK")
        self.assertTrue(magic_link_response[0] is not None)
        self.assertTrue(hasattr(magic_link_response[0], 'link'))
        self.assertTrue(hasattr(magic_link_response[0], 'expiry'))

    def test_delete_connected_account_with_connected_account_id(self):
        """ Method to test delete connected account with connected_account_id parameter """
        connected_account = self._create_oauth_connected_account()
        delete_identifier = f"delete_with_id_test_{self.test_identifier}"
        
        # First create a connected account
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=delete_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        created_account_id = create_response[0].connected_account.id
        
        # Now delete it using connected_account_id
        delete_response = self.scalekit_client.connected_accounts.delete_connected_account(
            connector=self.test_connector,
            identifier=delete_identifier,
            connected_account_id=created_account_id
        )
        self.assertEqual(delete_response[1].code().name, "OK")
        self.assertTrue(delete_response[0] is not None)

    def test_backward_compatibility_without_connected_account_id(self):
        """ Method to test that all methods still work without connected_account_id (backward compatibility) """
        connected_account = self._create_oauth_connected_account()
        compat_identifier = f"compat_test_{self.test_identifier}"
        
        # Test create (no connected_account_id parameter in create, so this is just baseline)
        create_response = self.scalekit_client.connected_accounts.create_connected_account(
            connector=self.test_connector,
            identifier=compat_identifier,
            connected_account=connected_account
        )
        self.assertEqual(create_response[1].code().name, "OK")
        
        # Test get without connected_account_id (backward compatibility)
        get_response = self.scalekit_client.connected_accounts.get_connected_account_by_identifier(
            connector=self.test_connector,
            identifier=compat_identifier
        )
        self.assertEqual(get_response[1].code().name, "OK")
        self.assertTrue(hasattr(get_response[0], 'connected_account'))
        
        # Test magic link without connected_account_id (backward compatibility)  
        magic_link_response = self.scalekit_client.connected_accounts.get_magic_link_for_connected_account(
            connector=self.test_connector,
            identifier=compat_identifier
        )
        self.assertEqual(magic_link_response[1].code().name, "OK")
        self.assertTrue(hasattr(magic_link_response[0], 'link'))
        
        # Test update without connected_account_id (backward compatibility)
        updated_oauth_token = OauthToken(
            access_token="compat_updated_access_token",
            refresh_token="compat_updated_refresh_token",
            scopes=["read", "write"]
        )
        updated_auth_details = AuthorizationDetails(oauth_token=updated_oauth_token)
        update_connected_account = UpdateConnectedAccount(authorization_details=updated_auth_details)
        
        update_response = self.scalekit_client.connected_accounts.update_connected_account(
            connector=self.test_connector,
            identifier=compat_identifier,
            connected_account=update_connected_account
        )
        self.assertEqual(update_response[1].code().name, "OK")
        
        # Test delete without connected_account_id (backward compatibility)
        delete_response = self.scalekit_client.connected_accounts.delete_connected_account(
            connector=self.test_connector,
            identifier=compat_identifier
        )
        self.assertEqual(delete_response[1].code().name, "OK")