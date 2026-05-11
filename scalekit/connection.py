from typing import List, Optional

from scalekit.core import CoreClient
from scalekit.v1.connections.connections_pb2 import *
from scalekit.v1.connections.connections_pb2_grpc import ConnectionServiceStub


class ConnectionClient:
    """Class definition for Connection Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for connection client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.connection_service = ConnectionServiceStub(
            self.core_client.grpc_secure_channel
        )

    def get_connection(
        self, organization_id: str, conn_id: str
    ) -> GetConnectionResponse:
        """
        Method to get connection object

        :param organization_id  : Client organization id to get connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to get connection
        :type                   : ``` str ```
        :returns
            Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetConnection.with_call,
            GetConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def list_connections_by_domain(self, domain: str, include: Optional[str] = None) -> ListConnectionsResponse:
        """
        Method to get connection object by domain

        :param domain     : Client domain id to get connections
        :type             : ``` str ```
        :param include    : Return active connections or all, E.g. - 'all'
        :type             : ``` str ```

        :returns:
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(domain=domain, include=include),
        )

    def list_connections(self, organization_id: str, include: Optional[str] = None) -> ListConnectionsResponse:
        """
        Method to list connections

        :param organization_id : Client organization id to get connections
        :type                  : ``` str ```
        :param include         : Return active connections or all, E.g. - 'all'
        :type                  : ``` str ```

        :returns:
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(organization_id=organization_id, include=include),
        )

    def enable_connection(
        self, organization_id: str, conn_id: str
    ) -> ToggleConnectionResponse:
        """
        Method to enable connection

        :param organization_id  : Client organization id to enable connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to enable connection
        :type                   : ``` str ```
        :returns
            Enable Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.EnableConnection.with_call,
            ToggleConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def disable_connection(
        self, organization_id: str, conn_id: str
    ) -> ToggleConnectionResponse:
        """
        Method to disable connection

        :param organization_id  : Client organization id to disable connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to disable connection
        :type                   : ``` str ```
        :returns
            Disable Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.DisableConnection.with_call,
            ToggleConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def create_connection(self, organization_id: str, connection: CreateConnection) -> CreateConnectionResponse:
        """
        Method to create a new connection

        :param organization_id  : Organization id to create connection for
        :type                   : ``` str ```
        :param connection       : CreateConnection object with expected values for conn creation
        :type                   : ``` obj ```

        :returns:
            Create Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.CreateConnection.with_call,
            CreateConnectionRequest(organization_id=organization_id, connection=connection),
        )
    
    def delete_connection(self, organization_id: str, connection_id: str):
        """
        Method to delete a connection based in given organization and connection id

        :param organization_id  : Organization id to delete connection for
        :type                   : ``` str ```
        :param connection_id    : Connection id of connection to be deleted
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.connection_service.DeleteConnection.with_call,
            DeleteConnectionRequest(organization_id=organization_id, id=connection_id),
        )

    def create_environment_connection(
        self,
        connection: CreateConnection,
        flags: Optional[Flags] = None,
    ) -> CreateConnectionResponse:
        """
        Create an SSO connection at the environment level without tying it to a specific organization.

        When to use: Call when setting up a shared connection that applies environment-wide
        rather than to a single tenant.

        :param connection  : CreateConnection object specifying provider, type, and config
        :type              : ``` CreateConnection ```
        :param flags       : Optional Flags object to control connection behavior (e.g. skip_attribute_mapping)
        :type              : ``` Flags | None ```

        :returns:
            CreateConnectionResponse — connection (Connection object with id, provider, type,
            status, and configuration details)
        """
        return self.core_client.grpc_exec(
            self.connection_service.CreateEnvironmentConnection.with_call,
            CreateEnvironmentConnectionRequest(connection=connection, flags=flags),
        )

    def assign_domains_to_connection(
        self,
        organization_id: str,
        connection_id: str,
        domain_ids: List[str],
    ) -> AssignDomainsToConnectionResponse:
        """
        Assign one or more verified domains to a connection so SSO is triggered for those domains.

        When to use: Call after verifying a domain and creating the connection to wire them
        together so users from that domain get routed to the correct IdP.

        :param organization_id  : ID of the organization that owns the connection
        :type                   : ``` str ```
        :param connection_id    : ID of the connection to assign domains to
        :type                   : ``` str ```
        :param domain_ids       : List of verified domain IDs to associate with this connection
        :type                   : ``` list[str] ```

        :returns:
            AssignDomainsToConnectionResponse — connection (updated Connection object
            reflecting the newly assigned domains)
        """
        return self.core_client.grpc_exec(
            self.connection_service.AssignDomainsToConnection.with_call,
            AssignDomainsToConnectionRequest(
                organization_id=organization_id,
                connection_id=connection_id,
                domain_ids=domain_ids,
            ),
        )

    def get_environment_connection(self, connection_id: str) -> GetConnectionResponse:
        """
        Fetch a single environment-level connection by its ID.

        When to use: Call when displaying connection details in the admin UI for a
        connection that was created at the environment scope.

        :param connection_id  : ID of the environment connection to fetch
        :type                 : ``` str ```

        :returns:
            GetConnectionResponse — connection (Connection object with provider, type,
            status, enabled flag, and full configuration)
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetEnvironmentConnection.with_call,
            GetEnvironmentConnectionRequest(connection_id=connection_id),
        )

    def list_organization_connections(
        self,
        page_size: int = 20,
        page_token: Optional[str] = None,
    ) -> ListOrganizationConnectionsResponse:
        """
        List all SSO connections across all organizations in the environment.

        When to use: Call when building an admin overview page that shows all tenant
        connections without filtering to a specific organization.

        :param page_size   : Maximum number of results to return per page (default 20)
        :type              : ``` int ```
        :param page_token  : Pagination cursor from a previous response's next_page_token
        :type              : ``` str | None ```

        :returns:
            ListOrganizationConnectionsResponse — connections (list of Connection objects),
            total_size, next_page_token, and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListOrganizationConnections.with_call,
            ListOrganizationConnectionsRequest(
                page_size=page_size,
                page_token=page_token,
            ),
        )

    def search_organization_connections(
        self,
        query: Optional[str] = None,
        provider: Optional[str] = None,
        status: Optional[str] = None,
        connection_type: Optional[str] = None,
        enabled: Optional[bool] = None,
        page_size: int = 20,
        page_token: Optional[str] = None,
    ) -> SearchOrganizationConnectionsResponse:
        """
        Search SSO connections across all organizations using filters.

        When to use: Call when building a filtered connection list in the admin UI,
        e.g. "show all enabled SAML connections for Okta".

        :param query           : Free-text search matched against connection name and org name
        :type                  : ``` str | None ```
        :param provider        : Filter by identity provider (e.g. "OKTA", "AZURE_AD")
        :type                  : ``` str | None ```
        :param status          : Filter by connection status (e.g. "ACTIVE", "INACTIVE")
        :type                  : ``` str | None ```
        :param connection_type : Filter by connection type (e.g. "SAML", "OIDC")
        :type                  : ``` str | None ```
        :param enabled         : Filter by enabled state (True for enabled only, False for disabled only)
        :type                  : ``` bool | None ```
        :param page_size       : Maximum number of results to return per page (default 20)
        :type                  : ``` int ```
        :param page_token      : Pagination cursor from a previous response's next_page_token
        :type                  : ``` str | None ```

        :returns:
            SearchOrganizationConnectionsResponse — connections (list of matching Connection objects),
            total_size, next_page_token, and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.connection_service.SearchOrganizationConnections.with_call,
            SearchOrganizationConnectionsRequest(
                query=query,
                provider=provider,
                status=status,
                connection_type=connection_type,
                enabled=enabled,
                page_size=page_size,
                page_token=page_token,
            ),
        )

    def update_environment_connection(
        self,
        connection_id: str,
        connection: UpdateConnection,
    ) -> UpdateConnectionResponse:
        """
        Update an environment-level connection's configuration.

        When to use: Call when updating IdP metadata, attribute mappings, or other
        settings on a connection that was created at the environment scope.

        :param connection_id  : ID of the environment connection to update
        :type                 : ``` str ```
        :param connection     : UpdateConnection object containing the fields to update
        :type                 : ``` UpdateConnection ```

        :returns:
            UpdateConnectionResponse — connection (updated Connection object with all current fields)
        """
        return self.core_client.grpc_exec(
            self.connection_service.UpdateEnvironmentConnection.with_call,
            UpdateEnvironmentConnectionRequest(
                connection_id=connection_id,
                connection=connection,
            ),
        )

    def update_connection(
        self,
        organization_id: str,
        connection_id: str,
        connection: UpdateConnection,
    ) -> UpdateConnectionResponse:
        """
        Update an organization-scoped SSO connection's configuration.

        When to use: Call when a customer changes their IdP metadata URL, signing
        certificates, or attribute mappings through the admin portal.

        :param organization_id  : ID of the organization that owns the connection
        :type                   : ``` str ```
        :param connection_id    : ID of the connection to update
        :type                   : ``` str ```
        :param connection       : UpdateConnection object with the fields to update
        :type                   : ``` UpdateConnection ```

        :returns:
            UpdateConnectionResponse — connection (updated Connection object)
        """
        return self.core_client.grpc_exec(
            self.connection_service.UpdateConnection.with_call,
            UpdateConnectionRequest(
                organization_id=organization_id,
                id=connection_id,
                connection=connection,
            ),
        )

    def delete_environment_connection(self, connection_id: str):
        """
        Delete an environment-level connection permanently.

        When to use: Call when removing a shared environment connection that is no
        longer needed.

        :param connection_id  : ID of the environment connection to delete
        :type                 : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.connection_service.DeleteEnvironmentConnection.with_call,
            DeleteEnvironmentConnectionRequest(connection_id=connection_id),
        )

    def enable_environment_connection(self, connection_id: str) -> ToggleConnectionResponse:
        """
        Enable an environment-level connection so it can process authentication requests.

        When to use: Call after finishing configuration of an environment connection
        to make it active in the auth flow.

        :param connection_id  : ID of the environment connection to enable
        :type                 : ``` str ```

        :returns:
            ToggleConnectionResponse — enabled (bool confirming the new state),
            error_message (non-empty string if enabling failed)
        """
        return self.core_client.grpc_exec(
            self.connection_service.EnableEnvironmentConnection.with_call,
            ToggleEnvironmentConnectionRequest(connection_id=connection_id),
        )

    def disable_environment_connection(self, connection_id: str) -> ToggleConnectionResponse:
        """
        Disable an environment-level connection so it stops processing authentication requests.

        When to use: Call when temporarily suspending an environment connection
        without deleting its configuration.

        :param connection_id  : ID of the environment connection to disable
        :type                 : ``` str ```

        :returns:
            ToggleConnectionResponse — enabled (bool confirming the new state),
            error_message (non-empty string if disabling failed)
        """
        return self.core_client.grpc_exec(
            self.connection_service.DisableEnvironmentConnection.with_call,
            ToggleEnvironmentConnectionRequest(connection_id=connection_id),
        )

    def get_connection_test_result(
        self,
        connection_id: str,
        test_request_id: str,
    ) -> GetConnectionTestResultResponse:
        """
        Retrieve the result of a previously initiated connection test.

        When to use: Call after triggering a test login to check whether the IdP
        connection is correctly configured — poll until status is terminal.

        :param connection_id     : ID of the connection that was tested
        :type                    : ``` str ```
        :param test_request_id   : ID of the test request returned when the test was initiated
        :type                    : ``` str ```

        :returns:
            GetConnectionTestResultResponse — status (TestResultStatus enum),
            user_info (attributes returned by the IdP during the test),
            error and error_description (set on failure),
            error_details (list of structured error detail messages)
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetConnectionTestResult.with_call,
            GetConnectionTestResultRequest(
                connection_id=connection_id,
                test_request_id=test_request_id,
            ),
        )

    def list_app_connections(
        self,
        page_size: int = 20,
        page_token: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> ListAppConnectionsResponse:
        """
        List connections available at the application (provider) level.

        When to use: Call when populating a login screen that lets users pick their
        social or enterprise provider (GitHub, Google, etc.).

        :param page_size   : Maximum number of results to return per page (default 20)
        :type              : ``` int ```
        :param page_token  : Pagination cursor from a previous response's next_page_token
        :type              : ``` str | None ```
        :param provider    : Filter by provider name (e.g. "GITHUB", "GOOGLE")
        :type              : ``` str | None ```

        :returns:
            ListAppConnectionsResponse — connections (list of Connection objects),
            total_size, next_page_token, and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListAppConnections.with_call,
            ListAppConnectionsRequest(
                page_size=page_size,
                page_token=page_token,
                provider=provider,
            ),
        )

    def get_connection_context(
        self,
        connection_id: str,
        organization_id: str,
    ) -> GetConnectionContextResponse:
        """
        Fetch the context object attached to a connection within an organization.

        When to use: Call when you need to read custom metadata or configuration stored
        on a connection for a specific organization (e.g. tenant-specific SCIM settings).

        :param connection_id    : ID of the connection to fetch context for
        :type                   : ``` str ```
        :param organization_id  : ID of the organization that scopes this connection context
        :type                   : ``` str ```

        :returns:
            GetConnectionContextResponse — context (structured object with custom
            key-value metadata attached to the connection)
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetConnectionContext.with_call,
            GetConnectionContextRequest(
                connection_id=connection_id,
                organization_id=organization_id,
            ),
        )

    def update_connection_context(
        self,
        connection_id: str,
        organization_id: str,
        context,
    ):
        """
        Update the context object attached to a connection within an organization.

        When to use: Call when storing custom configuration or metadata on a connection
        for a specific tenant (e.g. saving SCIM attribute mapping overrides).

        :param connection_id    : ID of the connection to update context for
        :type                   : ``` str ```
        :param organization_id  : ID of the organization that scopes this connection context
        :type                   : ``` str ```
        :param context          : Context object with the updated key-value metadata to store
        :type                   : context message object

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.connection_service.UpdateConnectionContext.with_call,
            UpdateConnectionContextRequest(
                connection_id=connection_id,
                organization_id=organization_id,
                context=context,
            ),
        )
