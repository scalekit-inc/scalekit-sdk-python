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

        :param display_name: Human-readable name for the provider. Required.
                             Accepted characters: a-z, A-Z, 0-9, and spaces.
                             Good practice: suffix with 'MCP' for MCP server providers.
        :type display_name: str
        :param proxy_url: Base HTTPS URL of the provider's server. Required.
        :type proxy_url: str
        :param proxy_enabled: Whether to enable Scalekit request proxying. Defaults to True.
        :type proxy_enabled: bool
        :param description: Short description of the provider. Defaults to empty string.
        :type description: str
        :param auth_patterns: Authentication options available to users. Each element
                               must be an AuthPattern instance. Currently only a single
                               AuthPattern is supported — pass a list with exactly one
                               element. The list type is intentional for future
                               multi-pattern support. Optional.
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
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        proxy_url: Optional[str] = None,
        auth_patterns: Optional[List[AuthPattern]] = None,
        icon_src: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        """Update an existing custom provider.

        Only fields explicitly passed with a non-None value are applied to the
        provider. Fields left as None are not included in the update request and
        the server keeps their existing values.

        :param identifier: Identifier of the custom provider to update. Required.
        :type identifier: str
        :param display_name: New display name. Accepted characters: a-z, A-Z, 0-9,
                             and spaces. Good practice: suffix with 'MCP' for MCP
                             server providers. Pass None to leave unchanged.
        :type display_name: Optional[str]
        :param description: New description. Pass None to leave unchanged.
        :type description: Optional[str]
        :param proxy_url: New proxy URL. Pass None to leave unchanged.
        :type proxy_url: Optional[str]
        :param auth_patterns: Replacement auth patterns. Fully replaces the existing
                               list when provided — it is not merged. Currently only a
                               single AuthPattern is supported — pass a list with exactly
                               one element. The list type is intentional for future
                               multi-pattern support. Pass None to leave unchanged.
        :type auth_patterns: Optional[List[AuthPattern]]
        :param icon_src: New icon URL. Pass None to leave unchanged.
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
        provider = UpdateCustomProvider()
        if display_name is not None:
            provider.display_name = display_name
        if description is not None:
            provider.description = description
        if proxy_url is not None:
            provider.proxy_url = proxy_url
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
        and can no longer be used for new connections.

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
                              ProviderType.ALL=2. Pass None to return all.
        :type provider_type: Optional[int]
        :param identifier: Filter to a specific provider by identifier.
                           Pass None to return all providers.
        :type identifier: Optional[str]

        :returns: Tuple of (ListProvidersResponse proto, grpc.Call).
                  response[0].providers contains the list of provider protos.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        filter_obj = None
        if provider_type is not None:
            filter_obj = ListProvidersRequest.Filter(provider_type=provider_type)
        return self.core_client.grpc_exec(
            self._stub.ListProviders.with_call,
            ListProvidersRequest(
                identifier=identifier or "",
                page_size=page_size or 0,
                page_token=page_token or "",
                filter=filter_obj,
            ),
        )
