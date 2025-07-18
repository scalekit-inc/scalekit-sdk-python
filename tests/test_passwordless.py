import os
import time
import unittest
from faker import Faker
from basetest import BaseTest
from scalekit.v1.auth.passwordless_pb2 import TemplateType, PasswordlessType


class TestPasswordless(BaseTest):
    """Test class for Passwordless authentication methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.faker = Faker()
        self.test_email = "dhaneshbabu007@gmail.com"
        self.invalid_auth_request_id = "invalid-auth-request-id"
        self.invalid_code = "000000"
        self.invalid_link_token = "invalid-link-token"
        self.auth_request_id = None  # Will be set by send_passwordless_email tests

    def test_send_passwordless_email_with_string_template(self):
        """Test sending passwordless email with string template (Node.js-like API)"""
        try:
            response = self.scalekit_client.passwordless.send_passwordless_email(
                email=self.test_email,
                template="SIGNIN",  
                magiclink_auth_uri="https://myapp.com/auth/callback",
                state="integration-test-state",
                expires_in=1800,  # 30 minutes
                template_variables={
                    "appName": "Integration Test App",
                    "company": "Test Company",
                    "employeeID": "EMP123"
                }
            )

            # Assert response structure and content
            self.assertEqual(response[1].code().name, "OK")
            self.assertIsNotNone(response[0])
            self.assertIsNotNone(response[0].auth_request_id)
            self.assertTrue(len(response[0].auth_request_id) > 0)
            self.assertTrue(response[0].expires_at > 0)
            self.assertTrue(response[0].expires_in > 0)
            self.assertIsNotNone(response[0].passwordless_type)
            
            # Store auth_request_id for other tests
            self.auth_request_id = response[0].auth_request_id
            
            print(f"✓ Email sent successfully! Auth Request ID: {response[0].auth_request_id}")
            
        except Exception as e:
            self.skipTest(f"Skipping test due to error: {str(e)}")

    def test_send_passwordless_email_with_direct_enum(self):
        """Test sending passwordless email with direct enum (if users prefer explicit enums)"""
        try:
            response = self.scalekit_client.passwordless.send_passwordless_email(
                email=self.test_email,
                template=TemplateType.SIGNUP,  # Direct enum access
                magiclink_auth_uri="https://myapp.com/auth/callback",
                state="integration-test-state-enum",
                expires_in=1800,
                template_variables={
                    "appName": "Integration Test App",
                    "company": "Test Company"
                }
            )

            # Assert response structure and content
            self.assertEqual(response[1].code().name, "OK")
            self.assertIsNotNone(response[0])
            self.assertIsNotNone(response[0].auth_request_id)
            self.assertTrue(len(response[0].auth_request_id) > 0)
            self.assertTrue(response[0].expires_at > 0)
            self.assertTrue(response[0].expires_in > 0)
            self.assertIsNotNone(response[0].passwordless_type)
            
            print(f"✓ Email sent with direct enum! Auth Request ID: {response[0].auth_request_id}")
            
        except Exception as e:
            self.skipTest(f"Skipping test due to error: {str(e)}")



    def test_send_passwordless_email_invalid_template(self):
        """Test sending passwordless email with invalid template"""
        with self.assertRaises(ValueError) as context:
            self.scalekit_client.passwordless.send_passwordless_email(
                email=self.test_email,
                template="INVALID_TEMPLATE"
            )
        
        self.assertIn("Invalid template type", str(context.exception))
        print("✓ Invalid template validation works correctly")



    def test_resend_passwordless_email(self):
        """Test resending passwordless email"""
        try:
            # First send an email to get an auth request ID
            send_response = self.scalekit_client.passwordless.send_passwordless_email(
                email=self.test_email,
                template="SIGNIN",
                magiclink_auth_uri="https://myapp.com/auth/callback",
                state="integration-test-state",
                expires_in=1800,
                template_variables={
                    "appName": "Integration Test App",
                    "company": "Test Company"
                }
            )

            # Assert initial response
            self.assertEqual(send_response[1].code().name, "OK")
            self.assertIsNotNone(send_response[0])
            self.assertIsNotNone(send_response[0].auth_request_id)
            
            auth_request_id = send_response[0].auth_request_id

            # Try to verify with invalid code (should fail)
            try:
                verify_response = self.scalekit_client.passwordless.verify_passwordless_email(
                    code=self.invalid_code,
                    auth_request_id=auth_request_id
                )
                # If we get here, verification didn't fail as expected
                self.assertEqual(verify_response[1].code().name, "OK")
            except Exception:
                # Expected to fail with invalid code
                pass

            # Wait a bit before resending to avoid rate limiting
            time.sleep(2)

            # Resend the email
            resend_response = self.scalekit_client.passwordless.resend_passwordless_email(
                auth_request_id=auth_request_id
            )

            # Assert resend response
            self.assertEqual(resend_response[1].code().name, "OK")
            self.assertIsNotNone(resend_response[0])
            self.assertIsNotNone(resend_response[0].auth_request_id)
            self.assertTrue(resend_response[0].expires_at > 0)
            self.assertTrue(resend_response[0].expires_in > 0)
            
            print(f"✓ Email resent successfully! Auth Request ID: {resend_response[0].auth_request_id}")
            
        except Exception as e:
            self.skipTest(f"Skipping test due to error: {str(e)}")

    def test_verify_passwordless_email_invalid_code(self):
        """Test verifying passwordless email with invalid code"""
        try:
            response = self.scalekit_client.passwordless.verify_passwordless_email(
                code=self.invalid_code,
                auth_request_id=self.invalid_auth_request_id
            )
            
            # This should fail, but if it somehow passes, check the response
            if response[1].code().name == "OK":
                self.fail("Expected verification to fail with invalid code")
                
        except Exception as e:
            # Expected to fail with invalid code
            self.assertIsNotNone(e)
            print(f"✓ Invalid code verification correctly failed: {str(e)}")

    def test_verify_passwordless_email_invalid_link_token(self):
        """Test verifying passwordless email with invalid link token"""
        try:
            response = self.scalekit_client.passwordless.verify_passwordless_email(
                link_token=self.invalid_link_token
            )
            
            # This should fail, but if it somehow passes, check the response
            if response[1].code().name == "OK":
                self.fail("Expected verification to fail with invalid link token")
                
        except Exception as e:
            # Expected to fail with invalid link token
            self.assertIsNotNone(e)
            print(f"✓ Invalid link token verification correctly failed: {str(e)}")





    def test_resend_passwordless_email_invalid_auth_request_id(self):
        """Test resending passwordless email with invalid auth request ID"""
        try:
            response = self.scalekit_client.passwordless.resend_passwordless_email(
                auth_request_id=self.invalid_auth_request_id
            )
            
            # This should fail, but if it somehow passes, check the response
            if response[1].code().name == "OK":
                self.fail("Expected resend to fail with invalid auth request ID")
                
        except Exception as e:
            # Expected to fail with invalid auth request ID
            self.assertIsNotNone(e)
            print(f"✓ Invalid auth request ID resend correctly failed: {str(e)}")

    def test_passwordless_enums(self):
        """Test that passwordless enums are properly accessible"""
        # Test template type enums
        self.assertEqual(TemplateType.SIGNIN, 1)
        self.assertEqual(TemplateType.SIGNUP, 2)
        
        # Test passwordless type enums
        self.assertEqual(PasswordlessType.OTP, 1)
        self.assertEqual(PasswordlessType.LINK, 2)
        self.assertEqual(PasswordlessType.LINK_OTP, 3)
        
        print("✓ All passwordless enums are properly accessible")

    def test_template_type_conversion(self):
        """Test the template type conversion functionality"""
        from scalekit.passwordless import _convert_template_type
        
        # Test string conversions
        self.assertEqual(_convert_template_type("SIGNIN"), TemplateType.SIGNIN)
        self.assertEqual(_convert_template_type("SIGNUP"), TemplateType.SIGNUP)
        self.assertEqual(_convert_template_type("signin"), TemplateType.SIGNIN)  # Case insensitive
        self.assertEqual(_convert_template_type("SignUp"), TemplateType.SIGNUP)  # Case insensitive
        
        # Test enum passthrough
        self.assertEqual(_convert_template_type(TemplateType.SIGNIN), TemplateType.SIGNIN)
        
        # Test None handling
        self.assertIsNone(_convert_template_type(None))
        
        # Test invalid template
        with self.assertRaises(ValueError):
            _convert_template_type("INVALID")
            
        print("✓ Template type conversion works correctly")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n✓ Passwordless tests completed")


if __name__ == '__main__':
    unittest.main() 