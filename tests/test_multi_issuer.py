"""
Tests for multi-issuer token validation.

`TokenValidationOptions.issuer` accepts a str or a list of str. A token is valid
if its `iss` claim exactly equals any configured issuer. An unset, empty-string or
empty-list issuer skips the issuer check.

These tests never touch the network: client auth and gRPC channel creation are
mocked and the signing key is generated locally.
"""
import time
import unittest
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from scalekit import ScalekitClient
from scalekit.common.exceptions import ScalekitValidateTokenFailureException
from scalekit.common.scalekit import TokenValidationOptions
from scalekit.core import CoreClient

ENV_URL = "https://acme.scalekit.cloud"
BASE_ISSUER = ENV_URL
RESOURCE_ISSUER = f"{ENV_URL}/resources/res_123"
KID = "test-key-1"


def _build_client():
    with patch.object(CoreClient, "_CoreClient__authenticate_client"), \
            patch("scalekit.core.grpc.secure_channel"), \
            patch("scalekit.core.grpc.ssl_channel_credentials"), \
            patch("scalekit.core.grpc.access_token_call_credentials"), \
            patch("scalekit.core.grpc.composite_channel_credentials"):
        return ScalekitClient(ENV_URL, "cid", "csec")


class TestMultiIssuerValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.private_pem = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        cls.public_pem = private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def setUp(self):
        self.client = _build_client()
        # Pre-populate keys so CoreClient.get_jwks() short-circuits without network
        self.client.core_client.keys = {KID: self.public_pem}

    def _sign(self, iss):
        now = int(time.time())
        return jwt.encode(
            {"sub": "user_1", "iss": iss, "iat": now, "exp": now + 3600},
            self.private_pem,
            algorithm="RS256",
            headers={"kid": KID},
        )

    def _claims(self, token, issuer):
        return self.client.validate_access_token_and_get_claims(
            token, options=TokenValidationOptions(issuer=issuer)
        )

    def _valid(self, token, issuer):
        return self.client.validate_access_token(
            token, options=TokenValidationOptions(issuer=issuer)
        )

    # --- single string (existing behavior) ---

    def test_single_issuer_match(self):
        token = self._sign(BASE_ISSUER)
        self.assertEqual(self._claims(token, BASE_ISSUER)["sub"], "user_1")
        self.assertTrue(self._valid(token, BASE_ISSUER))

    def test_single_issuer_mismatch(self):
        token = self._sign(BASE_ISSUER)
        self.assertFalse(self._valid(token, RESOURCE_ISSUER))
        with self.assertRaises(ScalekitValidateTokenFailureException):
            self._claims(token, RESOURCE_ISSUER)

    # --- list of issuers ---

    def test_list_matches_first_entry(self):
        token = self._sign(BASE_ISSUER)
        issuers = [BASE_ISSUER, RESOURCE_ISSUER]
        self.assertEqual(self._claims(token, issuers)["sub"], "user_1")
        self.assertTrue(self._valid(token, issuers))

    def test_list_matches_second_entry_resource_scoped_token(self):
        token = self._sign(RESOURCE_ISSUER)
        issuers = [BASE_ISSUER, RESOURCE_ISSUER]
        self.assertEqual(self._claims(token, issuers)["sub"], "user_1")
        self.assertTrue(self._valid(token, issuers))

    def test_list_matches_none(self):
        token = self._sign(f"{ENV_URL}/resources/res_other")
        issuers = [BASE_ISSUER, RESOURCE_ISSUER]
        self.assertFalse(self._valid(token, issuers))
        with self.assertRaises(ScalekitValidateTokenFailureException):
            self._claims(token, issuers)

    def test_no_trailing_slash_normalization(self):
        token = self._sign(BASE_ISSUER + "/")
        self.assertFalse(self._valid(token, [BASE_ISSUER]))

    # --- issuer check skipped ---

    def test_none_issuer_skips_check(self):
        token = self._sign(RESOURCE_ISSUER)
        self.assertTrue(self._valid(token, None))

    def test_empty_list_skips_check(self):
        token = self._sign(RESOURCE_ISSUER)
        self.assertTrue(self._valid(token, []))
        self.assertEqual(self._claims(token, [])["sub"], "user_1")

    def test_empty_string_skips_check(self):
        token = self._sign(RESOURCE_ISSUER)
        self.assertTrue(self._valid(token, ""))


if __name__ == "__main__":
    unittest.main()
