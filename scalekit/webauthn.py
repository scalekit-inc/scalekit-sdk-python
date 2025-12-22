from scalekit.core import CoreClient
from scalekit.v1.auth import webauthn_pb2
from scalekit.v1.auth.webauthn_pb2_grpc import WebAuthnServiceStub


class WebAuthnClient:
    """Class definition for WebAuthn Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for WebAuthn Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.webauthn_service = WebAuthnServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_credentials(self, user_id: str) -> webauthn_pb2.ListCredentialsResponse:
        """
        Method to list WebAuthn credentials for a user

        :param user_id          : User ID to list credentials for
        :type                   : ``` str ```

        :returns:
            Tuple of (ListCredentialsResponse, grpc.Call metadata)
        """
        request = webauthn_pb2.ListCredentialsRequest(user_id=user_id)

        return self.core_client.grpc_exec(
            self.webauthn_service.ListCredentials.with_call,
            request,
        )

    def update_credential(
        self,
        credential_id: str,
        display_name: str,
    ) -> webauthn_pb2.UpdateCredentialResponse:
        """
        Method to update a WebAuthn credential's display name

        :param credential_id    : Credential ID to update
        :type                   : ``` str ```
        :param display_name     : New display name for the credential
        :type                   : ``` str ```

        :returns:
            Tuple of (UpdateCredentialResponse, grpc.Call metadata)
        """
        request = webauthn_pb2.UpdateCredentialRequest(
            credential_id=credential_id,
            display_name=display_name,
        )

        return self.core_client.grpc_exec(
            self.webauthn_service.UpdateCredential.with_call,
            request,
        )

    def delete_credential(
        self,
        credential_id: str,
    ) -> webauthn_pb2.DeleteCredentialResponse:
        """
        Method to delete a WebAuthn credential

        :param credential_id    : Credential ID to delete
        :type                   : ``` str ```

        :returns:
            Tuple of (DeleteCredentialResponse, grpc.Call metadata)
        """
        request = webauthn_pb2.DeleteCredentialRequest(credential_id=credential_id)

        return self.core_client.grpc_exec(
            self.webauthn_service.DeleteCredential.with_call,
            request,
        )

