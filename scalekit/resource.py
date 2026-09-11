from typing import Optional, List

from scalekit.core import CoreClient
from scalekit.v1.clients.clients_pb2 import *
from scalekit.v1.clients.clients_pb2_grpc import ClientServiceStub


class ResourceClient:
    """API to read and revoke end-user consents granted against a resource"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Resource Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.client_service = ClientServiceStub(self.core_client.grpc_secure_channel)

    def list_user_consents(
        self,
        resource_id: str,
        search: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        user_ids: Optional[List[str]] = None,
    ) -> ListResourceUserConsentsResponse:
        """
        Method to list the end-user consents granted against a resource

        Each returned consent carries id, external_user_id, client_id, client_name,
        scopes and granted_at. The response also carries total_size plus
        next_page_token / prev_page_token cursors.

        Pass user_ids to match specific external user IDs exactly and
        case-sensitively. Pass search for a case-insensitive substring match.
        When both are given, user_ids wins and search is ignored.

        :param resource_id      : Resource id to list consents for (format: res_xxxxx)
        :type                   : ``` str ```
        :param search           : Case-insensitive substring match on external user IDs
        :type                   : ``` str ```
        :param page_size        : Page size for pagination (max 30)
        :type                   : ``` int ```
        :param page_token       : Page token for pagination
        :type                   : ``` str ```
        :param user_ids         : Exact match on external user IDs (max 25)
        :type                   : ``` list ```
        :returns:
            List Resource User Consents Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")

        return self.core_client.grpc_exec(
            self.client_service.ListResourceUserConsents.with_call,
            ListResourceUserConsentsRequest(
                resource_id=resource_id,
                search=search,
                page_size=page_size,
                page_token=page_token,
                filter=ResourceUserConsentFilter(external_user_id=user_ids) if user_ids else None,
            )
        )

    def revoke_user_consent(self, client_id: str, consent_id: str) -> RevokeUserConsentResponse:
        """
        Method to revoke a single end-user consent held by an API client

        Deletes the consent, so the client is prompted for consent again on its next
        authorization attempt, and revokes every active refresh token issued to that
        client for the same user. Access tokens already issued stay valid until they
        expire.

        Note that client_id is the API client that holds the consent, not the
        resource id.

        :param client_id        : Client holding the consent (format: m2m_xxxxx)
        :type                   : ``` str ```
        :param consent_id       : Consent to revoke (format: usrcnst_xxxxx)
        :type                   : ``` str ```
        :returns:
            Revoke User Consent Response
        """
        if not client_id:
            raise ValueError("client_id is required")
        if not consent_id:
            raise ValueError("consent_id is required")

        return self.core_client.grpc_exec(
            self.client_service.RevokeUserConsent.with_call,
            RevokeUserConsentRequest(client_id=client_id, consent_id=consent_id)
        )
