import base64
import unittest

from scalekit.middleware.session_crypto import (
    InvalidSessionError,
    decrypt_session,
    encrypt_session,
)


class TestSessionCrypto(unittest.TestCase):
    def setUp(self):
        self.secret = "correct-horse-battery-staple-secret"
        self.payload = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_123",
            "refresh_token": "rt_456",
            "expires_at": 9999999999,
        }

    def test_round_trip(self):
        token = encrypt_session(self.payload, self.secret)
        decrypted = decrypt_session(token, self.secret)
        self.assertEqual(decrypted, self.payload)

    def test_tampered_ciphertext_fails_to_decrypt(self):
        token = encrypt_session(self.payload, self.secret)
        raw = bytearray(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
        # flip a bit well inside the ciphertext (past version byte + nonce)
        raw[-1] ^= 0xFF
        tampered = base64.urlsafe_b64encode(bytes(raw)).decode("ascii").rstrip("=")

        with self.assertRaises(InvalidSessionError):
            decrypt_session(tampered, self.secret)

    def test_wrong_secret_fails_to_decrypt(self):
        token = encrypt_session(self.payload, self.secret)
        with self.assertRaises(InvalidSessionError):
            decrypt_session(token, "a-completely-different-secret")

    def test_missing_secret_raises_on_encrypt(self):
        with self.assertRaises(ValueError):
            encrypt_session(self.payload, "")

    def test_missing_secret_raises_on_decrypt(self):
        token = encrypt_session(self.payload, self.secret)
        with self.assertRaises(ValueError):
            decrypt_session(token, "")

    def test_missing_token_raises_invalid_session(self):
        with self.assertRaises(InvalidSessionError):
            decrypt_session("", self.secret)

    def test_malformed_token_raises_invalid_session_not_crash(self):
        with self.assertRaises(InvalidSessionError):
            decrypt_session("not-a-valid-base64url-token!!!", self.secret)

    def test_unsupported_version_byte_raises_invalid_session(self):
        token = encrypt_session(self.payload, self.secret)
        raw = bytearray(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
        raw[0] = 99  # bogus version
        bogus_version_token = base64.urlsafe_b64encode(bytes(raw)).decode("ascii").rstrip("=")

        with self.assertRaises(InvalidSessionError):
            decrypt_session(bogus_version_token, self.secret)

    def test_different_secrets_produce_non_decryptable_cross_over(self):
        # Simulates two server instances with mismatched secrets -- must fail
        # cleanly (InvalidSessionError), never crash, never silently succeed.
        token_a = encrypt_session(self.payload, "secret-a")
        with self.assertRaises(InvalidSessionError):
            decrypt_session(token_a, "secret-b")

    def test_oversized_payload_raises_instead_of_silently_dropping(self):
        # Browsers silently drop cookies over ~4096 bytes -- a customer with
        # many custom access-token claims could hit this. Must fail loudly at
        # encrypt time instead of producing a cookie the browser discards.
        oversized_payload = dict(self.payload)
        oversized_payload["user"] = {"claim": "x" * 4000}

        with self.assertRaises(ValueError):
            encrypt_session(oversized_payload, self.secret)


if __name__ == "__main__":
    unittest.main()
