from typing import Optional, List

from google.protobuf.field_mask_pb2 import FieldMask

from scalekit.core import CoreClient
from scalekit.v1.clients.clients_pb2 import *
# The proto message scalekit.v1.clients.ResourceClient shares its name with
# this file's own ResourceClient class below — the wildcard import above
# binds the proto message to that name first, but the `class ResourceClient`
# statement further down overwrites it in this module's namespace. Re-import
# the proto message under an alias so it stays reachable for type hints and
# for constructing request payloads.
from scalekit.v1.clients.clients_pb2 import ResourceClient as ResourceClientProto
from scalekit.v1.clients.clients_pb2_grpc import ClientServiceStub


class ResourceClient:
    """API to manage the API clients scoped to a resource, and to read and revoke end-user consents granted against one"""

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

    def create_resource_client(
        self, resource_id: str, client: ResourceClientProto
    ) -> CreateResourceClientResponse:
        """
        Method to create a new API client scoped to a resource

        Returns the created client plus a plain_secret — the plaintext
        client secret, only available at creation time. audience is ignored
        for MCP_SERVER/MCP_GATEWAY resources, which get their audience from
        the resource itself.

        :param resource_id  : Resource id to create the client for (format: res_xxxxx)
        :type               : ``` str ```
        :param client       : ResourceClient obj with the desired client properties defined
        :type               : ``` obj ```
        :returns:
            Create Resource Client Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")

        return self.core_client.grpc_exec(
            self.client_service.CreateResourceClient.with_call,
            CreateResourceClientRequest(resource_id=resource_id, client=client)
        )

    def get_resource_client(self, resource_id: str, client_id: str) -> GetResourceClientResponse:
        """
        Method to retrieve a single API client scoped to a resource, along with
        the end-users who have granted it consent

        :param resource_id  : Resource the client must belong to (format: res_xxxxx)
        :type               : ``` str ```
        :param client_id    : Client id (format: m2m_xxxxx)
        :type               : ``` str ```
        :returns:
            Get Resource Client Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")
        if not client_id:
            raise ValueError("client_id is required")

        return self.core_client.grpc_exec(
            self.client_service.GetResourceClient.with_call,
            GetResourceClientRequest(resource_id=resource_id, client_id=client_id)
        )

    def list_resource_clients(self, resource_id: str) -> ListResourceClientsResponse:
        """
        Method to list every API client scoped to a resource

        :param resource_id  : Resource whose clients to list (format: res_xxxxx)
        :type               : ``` str ```
        :returns:
            List Resource Clients Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")

        return self.core_client.grpc_exec(
            self.client_service.ListResourceClients.with_call,
            ListResourceClientsRequest(resource_id=resource_id)
        )

    def update_resource_client(
        self,
        resource_id: str,
        client_id: str,
        client: ResourceClientProto,
        update_mask: Optional[List[str]] = None,
    ) -> UpdateResourceClientResponse:
        """
        Method to update an existing API client scoped to a resource

        update_mask lists which fields of `client` to change, as raw field
        paths (e.g. ["scopes", "custom_claims"]). Verified against a live
        environment: the server only actually honors the mask for scopes,
        custom_claims and redirect_uris — include one of those paths with an
        empty value (e.g. scopes=[]) to clear it. name/description are
        applied whenever non-empty regardless of update_mask (an empty
        string is a no-op, not a clear), and audience is currently not
        applied on update at all, regardless of value or update_mask.

        :param resource_id  : Resource the client must belong to (format: res_xxxxx)
        :type               : ``` str ```
        :param client_id    : Client id to update
        :type               : ``` str ```
        :param client       : ResourceClient obj with the fields to update
        :type               : ``` obj ```
        :param update_mask  : Field paths in `client` to apply (see note above)
        :type               : ``` list ```
        :returns:
            Update Resource Client Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")
        if not client_id:
            raise ValueError("client_id is required")

        return self.core_client.grpc_exec(
            self.client_service.UpdateResourceClient.with_call,
            UpdateResourceClientRequest(
                resource_id=resource_id,
                client_id=client_id,
                client=client,
                update_mask=FieldMask(paths=update_mask) if update_mask else None,
            )
        )

    def delete_resource_client(self, resource_id: str, client_id: str) -> DeleteResourceClientResponse:
        """
        Method to permanently delete an API client scoped to a resource

        DeleteResourceClient shares its underlying delete path with client
        deletion in general, so nothing forces the given client_id to
        actually belong to resource_id. Since this method lives on
        `resources`, callers reasonably expect it to only ever touch clients
        within that resource — so this fetches the client first and verifies
        its own resource_id matches before deleting, refusing instead of
        trusting the id pair blindly.

        :param resource_id  : Resource the client must belong to (format: res_xxxxx)
        :type               : ``` str ```
        :param client_id    : Client id to delete
        :type               : ``` str ```
        :returns:
            Delete Resource Client Response
        """
        if not resource_id:
            raise ValueError("resource_id is required")
        if not client_id:
            raise ValueError("client_id is required")

        fetched = self.get_resource_client(resource_id, client_id)
        if fetched[0].client.resource_id != resource_id:
            raise ValueError(f"Client {client_id} does not belong to resource {resource_id}")

        return self.core_client.grpc_exec(
            self.client_service.DeleteResourceClient.with_call,
            DeleteResourceClientRequest(resource_id=resource_id, client_id=client_id)
        )

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
