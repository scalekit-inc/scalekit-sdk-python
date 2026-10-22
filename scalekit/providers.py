from typing import Dict, List, Optional

from google.protobuf import struct_pb2
from google.protobuf.json_format import ParseDict

from scalekit.actions.models.custom_provider import AuthPattern
from scalekit.core import CoreClient
from scalekit.v1.providers.providers_pb2 import (
    CreateCustomProvider,
    CreateCustomProviderRequest,
    UpdateCustomProvider,
    UpdateCustomProviderRequest,
    DeleteProviderRequest,
    ListProvidersRequest,
)
from scalekit.v1.providers.providers_pb2_grpc import ProviderServiceStub


def _patterns_to_list_value(patterns: List[AuthPattern]) -> struct_pb2.ListValue:
    return ParseDict([p.to_dict() for p in patterns], struct_pb2.ListValue())


class ProvidersClient:
    """Low-level gRPC client for custom provider CRUD operations.

    All methods return (proto_response, grpc.Call) tuples — the same convention
    used by every other sub-client in this SDK. Do not use this class directly;
    access it through ActionClient.providers which wraps it with typed
    request/response objects via ActionProviders.
    """

    def __init__(self, core_client: CoreClient):
        self.core_client = core_client
        self._stub = ProviderServiceStub(self.core_client.grpc_secure_channel)

    def create_custom_provider(
        self,
        display_name: str,
        proxy_url: str,
        proxy_enabled: bool = True,
        description: str = "",
        auth_patterns: Optional[List[AuthPattern]] = None,
        icon_src: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        """Create a new custom provider.

        :param display_name: Name shown in the UI. Required. Letters, digits and
                             spaces only (max 200 characters); symbols such as '_'
                             or '-' are rejected. The identifier is derived from it
                             ('Acme MCP' becomes 'ACMEMCP:<environment id>'). The
                             names of the built-in login providers (Github, Google,
                             Gitlab, Microsoft, LinkedIn, Salesforce, Facebook) are
                             rejected; other built-in names such as Gmail are accepted.
                             Good practice: suffix with 'MCP' for MCP server providers.
        :type display_name: str
        :param proxy_url: HTTPS URL of the external service this provider connects
                          to, and the address Scalekit sends proxied requests to.
                          For an MCP connector this is the MCP server's URL; for an
                          API connector it is the API's base URL. Required.
        :type proxy_url: str
        :param proxy_enabled: Whether to enable Scalekit request proxying. Defaults to True.
        :type proxy_enabled: bool
        :param description: Short description of the provider. Defaults to empty string.
        :type description: str
        :param auth_patterns: Authentication options available to users. Each element
                               must be an AuthPattern instance. Currently only a single
                               AuthPattern is supported — pass a list with exactly one
                               element. The list type is intentional for future
                               multi-pattern support. Required in practice: leaving
                               it out fails with a validation error on
                               provider.auth_patterns, and an empty list fails with
                               'auth patterns cannot be empty'. The SDK checks
                               neither before sending.
        :type auth_patterns: Optional[List[AuthPattern]]
        :param icon_src: URL of the provider's icon image. Optional.
        :type icon_src: Optional[str]
        :param metadata: Arbitrary string key-value pairs attached to the provider. Optional.
        :type metadata: Optional[Dict[str, str]]

        :returns: Tuple of (CreateProviderResponse proto, grpc.Call).
                  response[0].provider contains the created provider proto.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        provider = CreateCustomProvider(
            display_name=display_name,
            description=description,
            proxy_url=proxy_url,
            proxy_enabled=proxy_enabled,
        )
        if auth_patterns:
            provider.auth_patterns.CopyFrom(_patterns_to_list_value(auth_patterns))
        if icon_src is not None:
            provider.icon_src = icon_src
        if metadata:
            provider.metadata.update(metadata)
        return self.core_client.grpc_exec(
            self._stub.CreateCustomProvider.with_call,
            CreateCustomProviderRequest(provider=provider),
        )

    def update_custom_provider(
        self,
        identifier: str,
        display_name: str,
        proxy_url: str,
        description: Optional[str] = None,
        auth_patterns: Optional[List[AuthPattern]] = None,
        icon_src: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        """Update an existing custom provider.

        The server applies this as a PUT: it replaces the provider's settings and
        is not a partial update. Send display_name, proxy_url and auth_patterns
        every time. Fields left as None are not sent: description and icon_src
        are then kept, but metadata is cleared.

        :param identifier: Identifier of the custom provider to update. Required.
        :type identifier: str
        :param display_name: Name shown in the UI. Letters, digits and spaces only
                             (max 200 characters); symbols such as '_' or '-' are
                             rejected. Changing the name does not change the
                             identifier. Good practice: suffix with 'MCP' for MCP
                             server providers. Required.
        :type display_name: str
        :param proxy_url: HTTPS URL of the external service this provider connects
                          to, and the address Scalekit sends proxied requests to.
                          For an MCP connector this is the MCP server's URL; for an
                          API connector it is the API's base URL. Must start with
                          'https://'. Required.
        :type proxy_url: str
        :param description: New description. Pass None to leave unchanged. An empty
                            string does not clear it: the server ignores empty values.
        :type description: Optional[str]
        :param auth_patterns: Replacement auth patterns. Marked required by the API
                               on every update. Fully replaces the existing list — it
                               is not merged. Currently only a single AuthPattern is
                               supported — pass a list with exactly one element. The
                               list type is intentional for future multi-pattern
                               support. The auth type and is_mcp cannot be changed,
                               and an API_KEY provider cannot switch between
                               single-key and multiple-headers mode.
        :type auth_patterns: Optional[List[AuthPattern]]
        :param icon_src: New icon URL. Pass None to leave unchanged. An empty string
                         does not clear it.
        :type icon_src: Optional[str]
        :param metadata: Replacement metadata key-value pairs. The server replaces
                         the provider's entire metadata map with this value — it does
                         not merge. If omitted or set to None, the server clears all
                         existing metadata on the provider. To retain current metadata,
                         fetch the provider first and pass its metadata dict here.
        :type metadata: Optional[Dict[str, str]]

        :returns: Tuple of (UpdateProviderResponse proto, grpc.Call).
                  response[0].provider contains the updated provider proto.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        provider = UpdateCustomProvider(
            display_name=display_name,
            proxy_url=proxy_url,
            # Sent on every update.
            proxy_enabled=True,
        )
        if description is not None:
            provider.description = description
        if auth_patterns is not None:
            provider.auth_patterns.CopyFrom(_patterns_to_list_value(auth_patterns))
        if icon_src is not None:
            provider.icon_src = icon_src
        if metadata is not None:
            provider.metadata.update(metadata)
        return self.core_client.grpc_exec(
            self._stub.UpdateCustomProvider.with_call,
            UpdateCustomProviderRequest(identifier=identifier, provider=provider),
        )

    def delete_custom_provider(self, identifier: str):
        """Delete a custom provider by identifier.

        Deletion is permanent. The provider is removed from the Scalekit catalog
        and can no longer be used for new connections. The server refuses to delete
        a provider that still has connections, and a connection that still has
        connected accounts: remove the connected accounts, then the connections,
        then the provider. It also removes the provider's discovered custom MCP
        tools.

        :param identifier: Identifier of the custom provider to delete. Required.
        :type identifier: str

        :returns: Tuple of (DeleteProviderResponse proto, grpc.Call).
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        return self.core_client.grpc_exec(
            self._stub.DeleteCustomProvider.with_call,
            DeleteProviderRequest(identifier=identifier),
        )

    def list_providers(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        provider_type: Optional[int] = None,
        identifier: Optional[str] = None,
    ):
        """List providers, optionally filtered by type and identifier.

        :param page_size: Maximum number of providers to return. Pass None for
                          the server's default page size.
        :type page_size: Optional[int]
        :param page_token: Pagination cursor from a previous list response's
                           next_page_token. Pass None to fetch the first page.
        :type page_token: Optional[str]
        :param provider_type: ProviderType enum value to filter results.
                              ProviderType.CUSTOM=1, ProviderType.DEFAULT=0,
                              ProviderType.ALL=2. Pass None and only built-in
                              providers are returned (the same as DEFAULT): use
                              CUSTOM to find your own connectors, or ALL for both.
        :type provider_type: Optional[int]
        :param identifier: Filter to a specific provider by identifier.
                           Pass None to skip this filter.
        :type identifier: Optional[str]

        :returns: Tuple of (ListProvidersResponse proto, grpc.Call).
                  response[0].providers contains the list of provider protos.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        request = ListProvidersRequest(
            identifier=identifier or "",
            page_size=page_size or 0,
            page_token=page_token or "",
        )
        if provider_type is not None:
            request.filter.CopyFrom(ListProvidersRequest.Filter(provider_type=provider_type))
        return self.core_client.grpc_exec(
            self._stub.ListProviders.with_call,
            request,
        )
