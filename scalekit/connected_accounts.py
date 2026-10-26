from typing import List, Optional

from scalekit.core import CoreClient
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    CreateConnectedAccount,
    CreateConnectedAccountRequest,
    CreateConnectedAccountResponse,
    DeleteConnectedAccountRequest,
    DeleteConnectedAccountResponse,
    GetConnectedAccountByIdentifierRequest,
    GetConnectedAccountByIdentifierResponse,
    GetMagicLinkForConnectedAccountRequest,
    GetMagicLinkForConnectedAccountResponse,
    ListConnectedAccountsRequest,
    ListConnectedAccountsResponse,
    RefreshConnectedAccountTokensRequest,
    RefreshConnectedAccountTokensResponse,
    UpdateConnectedAccount,
    UpdateConnectedAccountRequest,
    UpdateConnectedAccountResponse,
    VerifyConnectedAccountUserRequest,
    VerifyConnectedAccountUserResponse,
)
from scalekit.v1.connected_accounts.connected_accounts_pb2_grpc import ConnectedAccountServiceStub


class ConnectedAccountsClient:
    """Class definition for Connected Accounts Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Connected Accounts Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.connected_accounts_service = ConnectedAccountServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_connected_accounts(
        self,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connector: Optional[str] = None,
        identifier: Optional[str] = None,
        provider: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        connection_names: Optional[List[str]] = None,
    ) -> ListConnectedAccountsResponse:
        """
        Method to list connected accounts for a user

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier (optional)
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector (optional)
        :type                   : ``` str ```
        :param provider         : Provider name (optional)
        :type                   : ``` str ```
        :param page_size        : Number of results per page (optional)
        :type                   : ``` int ```
        :param page_token       : Page token for pagination (optional)
        :type                   : ``` str ```
        :param connection_names : Filter results to only connected accounts belonging to these
                                  connection names (optional). Each entry is the slug name of
                                  a connector, e.g. ``["github", "google-calendar"]``.
        :type                   : ``` List[str] ```

        :returns:
            List Connected Accounts Response
        """
        request = ListConnectedAccountsRequest(
            organization_id=organization_id,
            user_id=user_id,
            connector=connector,
            identifier=identifier,
            provider=provider,
            page_size=page_size,
            page_token=page_token,
        )
        if connection_names:
            request.connection_names.extend(connection_names)
        return self.core_client.grpc_exec(
            self.connected_accounts_service.ListConnectedAccounts.with_call,
            request,
        )

    def create_connected_account(
        self,
        connector: str,
        identifier: str,
        connected_account: CreateConnectedAccount,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> CreateConnectedAccountResponse:
        """
        Method to create a connected account

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param connected_account: Connected account details
        :type                   : ``` CreateConnectedAccount ```

        :returns:
            Create Connected Account Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.CreateConnectedAccount.with_call,
            CreateConnectedAccountRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                connected_account=connected_account
            ),
        )

    def update_connected_account(
        self,
        connector: str,
        identifier: str,
        connected_account: UpdateConnectedAccount,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None
    ) -> UpdateConnectedAccountResponse:
        """
        Method to update a connected account

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param connected_account: Updated connected account details
        :type                   : ``` UpdateConnectedAccount ```
        :param connected_account_id : ID of the connected account to update
        :type                   : ``` str ```

        :returns:
            Update Connected Account Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.UpdateConnectedAccount.with_call,
            UpdateConnectedAccountRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                connected_account=connected_account,
                id=connected_account_id
            ),
        )

    def delete_connected_account(
        self,
        connector: str,
        identifier: str,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None
    ) -> DeleteConnectedAccountResponse:
        """
        Method to delete a connected account

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param connected_account_id : ID of the connected account to delete
        :type                   : ``` str ```

        :returns:
            Delete Connected Account Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.DeleteConnectedAccount.with_call,
            DeleteConnectedAccountRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                id=connected_account_id
            ),
        )

    def get_magic_link_for_connected_account(
        self,
        connector: str,
        identifier: str,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        state: Optional[str] = None,
        user_verify_url: Optional[str] = None
    ) -> GetMagicLinkForConnectedAccountResponse:
        """
        Method to get magic link for a connected account

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param connected_account_id : ID of the connected account
        :type                   : ``` str ```
        :param state            : Opaque state value passed through to the user verify redirect URL query params
        :type                   : ``` str ```
        :param user_verify_url  : B2B app's user verify redirect URL
        :type                   : ``` str ```

        :returns:
            Get Magic Link For Connected Account Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.GetMagicLinkForConnectedAccount.with_call,
            GetMagicLinkForConnectedAccountRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                id=connected_account_id,
                state=state,
                user_verify_url=user_verify_url
            ),
        )

    def get_connected_account_by_identifier(
        self,
        connector: str,
        identifier: str,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None
    ) -> GetConnectedAccountByIdentifierResponse:
        """
        Method to get connected account by identifier

        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param connected_account_id : ID of the connected account
        :type                   : ``` str ```

        :returns:
            Get Connected Account By Identifier Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.GetConnectedAccountAuth.with_call,
            GetConnectedAccountByIdentifierRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                id=connected_account_id
            ),
        )

    def get_connected_account_details_by_identifier(
        self,
        connector: str,
        identifier: str,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None
    ) -> GetConnectedAccountByIdentifierResponse:
        """
        Method to get connected account details (without auth credentials) by identifier

        :param connector        : Connector identifier
        :type                   : ``` str ```
        :param identifier       : Identifier for the connector
        :type                   : ``` str ```
        :param organization_id  : Organization ID
        :type                   : ``` str ```
        :param user_id          : User ID
        :type                   : ``` str ```
        :param connected_account_id : ID of the connected account
        :type                   : ``` str ```

        :returns:
            Get Connected Account By Identifier Response (without auth credentials)
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.GetConnectedAccountDetails.with_call,
            GetConnectedAccountByIdentifierRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                id=connected_account_id
            ),
        )

    def refresh_connected_account_tokens(
        self,
        connected_account_id: Optional[str] = None,
        connection_name: Optional[str] = None,
        identifier: Optional[str] = None
    ) -> RefreshConnectedAccountTokensResponse:
        """
        Method to refresh the stored tokens of a connected account now.

        Call this when a proxy call to the provider fails with an auth error, then
        retry the call. Identify the account by ``connected_account_id``, or by both
        ``connection_name`` and ``identifier``. If the ID is sent, the other two are ignored.

        Only ACTIVE accounts are refreshed. Key on ``error_code``, not only the HTTP status.
        Errors:

        - 400 REAUTHENTICATION_NEEDED: the account is EXPIRED (the user must authorize
          again; no provider call is made), or the provider rejected the refresh (for
          example invalid_grant, revoked, or no refresh token). In the second case the
          account is marked EXPIRED.
        - 500 INTERNAL_ERROR: provider outage, network error, 5xx or 429. The account
          stays ACTIVE; retry later.
        - 409 REFRESH_IN_PROGRESS: a refresh is already running for the account. Retry
          in a few seconds.
        - 400 REFRESH_NOT_SUPPORTED_FOR_CONNECTOR: API key, bearer, basic auth, no-auth
          and Trello OAuth1 accounts.
        - 403: account-bound or portal tokens. Use server-side API credentials.
        - 404: account not found.

        The response has account metadata only, no credentials; use ``token_expires_at``
        for the new expiry.

        :param connected_account_id : ID of the connected account
        :type                       : ``` str ```
        :param connection_name      : Connection name (use with identifier)
        :type                       : ``` str ```
        :param identifier           : Identifier for the connected account (use with connection_name)
        :type                       : ``` str ```

        :raises ValueError: If neither connected_account_id nor both connection_name
                            and identifier are given.

        :returns:
            Refresh Connected Account Tokens Response
        """
        if not connected_account_id and not (connection_name and identifier):
            raise ValueError(
                "connected_account_id, or both connection_name and identifier, is required"
            )
        if connected_account_id:
            request = RefreshConnectedAccountTokensRequest(
                connected_account_id=connected_account_id
            )
        else:
            request = RefreshConnectedAccountTokensRequest(
                connection_name=connection_name,
                identifier=identifier
            )
        return self.core_client.grpc_exec(
            self.connected_accounts_service.RefreshConnectedAccountTokens.with_call,
            request,
        )

    def verify_connected_account_user(
        self,
        auth_request_id: str,
        identifier: str
    ) -> VerifyConnectedAccountUserResponse:
        """
        Method to verify a connected account user after OAuth callback

        :param auth_request_id  : Auth request ID as base64url-encoded opaque token from the
                                  user verify redirect URL query params
        :type                   : ``` str ```
        :param identifier       : Current logged in user's connected account identifier
        :type                   : ``` str ```

        :returns:
            Verify Connected Account User Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.VerifyConnectedAccountUser.with_call,
            VerifyConnectedAccountUserRequest(
                auth_request_id=auth_request_id,
                identifier=identifier
            ),
        )
