import os
from basetest import BaseTest


class TestWebAuthnCredentials(BaseTest):
    """Class definition for Test WebAuthn Credentials"""

    def setUp(self):
        """Setup test parameters
        
        Test user and credential IDs must be provided via environment variables:
        - TEST_WEBAUTHN_USER_ID: User ID to test with (required)
        - TEST_WEBAUTHN_CREDENTIAL_ID: Credential ID to test with (required)
        
        Note: WebAuthn credentials must be pre-created as they require browser interaction.
        Set these in your .env file in the tests directory.
        """
        # Get from environment variables (required)
        self.test_user_id = os.environ.get('TEST_WEBAUTHN_USER_ID')
        self.test_credential_id = os.environ.get('TEST_WEBAUTHN_CREDENTIAL_ID')
        self.test_display_name = "Test Credential Updated"
        
        # Validate required user_id
        if not self.test_user_id:
            raise ValueError(
                "TEST_WEBAUTHN_USER_ID environment variable is required. "
                "Set it in your .env file in the tests directory."
            )
        
        # Validate required credential_id
        if not self.test_credential_id:
            raise ValueError(
                "TEST_WEBAUTHN_CREDENTIAL_ID environment variable is required. "
                "Set it in your .env file in the tests directory."
            )

    def test_list_credentials(self):
        """Method to test list credentials"""
        response = self.scalekit_client.webauthn.list_credentials(user_id=self.test_user_id)
        
        # Verify response structure
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'credentials'))
        self.assertTrue(hasattr(response[0], 'all_accepted_credentials_options'))
        
        # credentials found
        credentials = response[0].credentials
        
        for idx, cred in enumerate(credentials):
            assert cred.id is not None, f"Credential at index {idx} is missing 'id'"
            assert cred.user_id is not None, f"Credential at index {idx} is missing 'user_id'"
            assert cred.authenticator is not None, f"Credential at index {idx} is missing 'authenticator'"
        
        # Verify the test credential exists
        credential_ids = [cred.id for cred in credentials]
        self.assertIn(self.test_credential_id, credential_ids, f"Test credential {self.test_credential_id} not found in credentials list")

    def test_update_and_verify_credential(self):
        """Method to test update credential and verify it by listing
        
        This test performs both the update operation and verifies it by listing
        credentials, ensuring the update was persisted correctly.
        """
        # First, get the original credential to restore it later
        list_response = self.scalekit_client.webauthn.list_credentials(user_id=self.test_user_id)
        self.assertEqual(list_response[1].code().name, "OK")
        original_credential = None
        for cred in list_response[0].credentials:
            if cred.id == self.test_credential_id:
                original_credential = cred
                break
        
        self.assertIsNotNone(original_credential, "Test credential not found in list")
        original_display_name = original_credential.display_name if original_credential.display_name else "Test WebAuthn Cred"
        
        try:
            # Update the credential
            response = self.scalekit_client.webauthn.update_credential(
                credential_id=self.test_credential_id,
                display_name=self.test_display_name
            )
            
            # Verify response structure
            self.assertEqual(response[1].code().name, "OK")
            self.assertTrue(response[0] is not None)
            self.assertTrue(hasattr(response[0], 'credential'))
            
            # Verify the credential was updated in the response
            updated_credential = response[0].credential
            self.assertEqual(updated_credential.id, self.test_credential_id)
            self.assertEqual(updated_credential.display_name, self.test_display_name)
            
            # Verify the update by listing credentials again
            list_response = self.scalekit_client.webauthn.list_credentials(user_id=self.test_user_id)
            
            self.assertEqual(list_response[1].code().name, "OK")
            credentials = list_response[0].credentials
            
            # Find the updated credential in the list
            updated_cred = None
            for cred in credentials:
                if cred.id == self.test_credential_id:
                    updated_cred = cred
                    break
            
            self.assertIsNotNone(updated_cred, "Updated credential not found in list")
            self.assertEqual(updated_cred.display_name, self.test_display_name)
            
        finally:
            # Restore the original display name
            if original_credential is not None:
                try:
                    restore_response = self.scalekit_client.webauthn.update_credential(
                        credential_id=self.test_credential_id,
                        display_name=original_display_name
                    )
                except Exception as exp:
                    raise exp
