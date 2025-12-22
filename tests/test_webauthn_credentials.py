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
        print(f"\n=== Testing list_credentials for user_id: {self.test_user_id} ===")
        
        response = self.scalekit_client.webauthn.list_credentials(user_id=self.test_user_id)
        
        # Verify response structure
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'credentials'))
        self.assertTrue(hasattr(response[0], 'all_accepted_credentials_options'))
        
        # Print credentials found
        credentials = response[0].credentials
        print(f"Found {len(credentials)} credential(s)")
        
        for idx, cred in enumerate(credentials):
            print(f"\nCredential {idx + 1}:")
            print(f"  ID: {cred.id}")
            print(f"  User ID: {cred.user_id}")
            print(f"  Display Name: {cred.display_name if cred.display_name else '(not set)'}")
            print(f"  Attestation Type: {cred.attestation_type}")
            if cred.authenticator:
                print(f"  Authenticator: {cred.authenticator.name}")
            if cred.created_at:
                print(f"  Created At: {cred.created_at}")
        
        # Verify the test credential exists
        credential_ids = [cred.id for cred in credentials]
        self.assertIn(
            self.test_credential_id, 
            credential_ids,
            f"Test credential {self.test_credential_id} not found in credentials list"
        )
        
        print("\n✓ list_credentials test passed")

    def test_update_credential(self):
        """Method to test update credential"""
        print(f"\n=== Testing update_credential for credential_id: {self.test_credential_id} ===")
        
        response = self.scalekit_client.webauthn.update_credential(
            credential_id=self.test_credential_id,
            display_name=self.test_display_name
        )
        
        # Verify response structure
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'credential'))
        
        # Verify the credential was updated
        updated_credential = response[0].credential
        self.assertEqual(updated_credential.id, self.test_credential_id)
        self.assertEqual(updated_credential.display_name, self.test_display_name)
        
        print(f"Credential updated successfully:")
        print(f"  ID: {updated_credential.id}")
        print(f"  Display Name: {updated_credential.display_name}")
        print(f"  User ID: {updated_credential.user_id}")
        
        print("\n✓ update_credential test passed")

    def test_verify_update_by_listing(self):
        """Method to verify the update by listing credentials again"""
        print(f"\n=== Verifying update by listing credentials again ===")
        
        response = self.scalekit_client.webauthn.list_credentials(user_id=self.test_user_id)
        
        self.assertEqual(response[1].code().name, "OK")
        credentials = response[0].credentials
        
        # Find the updated credential
        updated_cred = None
        for cred in credentials:
            if cred.id == self.test_credential_id:
                updated_cred = cred
                break
        
        self.assertIsNotNone(updated_cred, "Updated credential not found in list")
        self.assertEqual(updated_cred.display_name, self.test_display_name)
        
        print(f"Verified: Credential display name is '{updated_cred.display_name}'")
        print("\n✓ verify_update_by_listing test passed")

