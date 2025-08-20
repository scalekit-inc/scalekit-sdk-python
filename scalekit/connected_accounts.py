from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.connected_accounts.connected_accounts_pb2 import *
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
        page_token: Optional[str] = None
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

        :returns:
            List Connected Accounts Response
        """
        return self.core_client.grpc_exec(
            self.connected_accounts_service.ListConnectedAccounts.with_call,
            ListConnectedAccountsRequest(
                organization_id=organization_id,
                user_id=user_id,
                connector=connector,
                identifier=identifier,
                provider=provider,
                page_size=page_size,
                page_token=page_token
            ),
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
        connected_account_id: Optional[str] = None
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
                id=connected_account_id
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