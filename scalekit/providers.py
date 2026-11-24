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
    # The wire form, not to_dict(): a pattern decoded from a response goes back exactly as the
    # server returned it, which an OpenAPI-sourced connector's update needs (see AuthPattern).
    return ParseDict([p._to_wire_dict() for p in patterns], struct_pb2.ListValue())


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
        proxy_url: Optional[str] = None,
        proxy_enabled: bool = True,
        description: str = "",
        auth_patterns: Optional[List[AuthPattern]] = None,
        icon_src: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        openapi_spec_url: Optional[str] = None,
    ):
        """Create a new custom provider.

        A custom connector is sourced from an MCP server (``proxy_url``) or from an
        OpenAPI spec (``openapi_spec_url``). Exactly one of the two is required;
        sending both, or neither, is rejected with 400 INVALID_ARGUMENT.

        For an OpenAPI-sourced connector the server fetches and validates the spec
        before it stores anything, returns immediately, and generates the tools in an
        asynchronous tool collection run that it queues for you. Follow that run with
        ``scalekit_client.actions.get_tool_collection_run``. The connector's base URL
        (``proxy_url`` on the returned provider) is filled in from the spec's own server
        URL by that run, only when that URL starts with https:// (otherwise it stays empty).
        Set or change it with update_custom_provider.

        Errors surface as ScalekitServerException subclasses: 400 INVALID_ARGUMENT for
        an invalid request, 400 FEATURE_NOT_ENABLED when OpenAPI-sourced connectors are
        not enabled for the environment, and 409 RESOURCE_ALREADY_EXISTS when an
        OpenAPI connector with the same name already exists in the environment.

        :param display_name: Name shown in the UI. Required. ASCII letters (a-z, A-Z),
                             digits and spaces only, 1-200 characters, with at least one
                             letter or digit; anything else, such as accented letters or
                             symbols like '_' or '-', is rejected. The identifier is
                             derived from it ('Acme MCP' becomes 'ACMEMCP:<environment
                             id>'). The names of the built-in login providers (Github,
                             Google, Gitlab, Microsoft, LinkedIn, Salesforce, Facebook)
                             are rejected; other built-in names such as Gmail are
                             accepted. Good practice: suffix with 'MCP' for MCP server
                             providers.
        :type display_name: str
        :param proxy_url: HTTPS URL of the external service this provider connects
                          to, and the address Scalekit sends proxied requests to.
                          For an MCP connector this is the MCP server's URL; for an
                          API connector it is the API's base URL. Must start with
                          'https://' (at most 2048 characters). Leave it out when
                          you pass ``openapi_spec_url``: the server rejects both together.
        :type proxy_url: Optional[str]
        :param proxy_enabled: Ignored. A custom connector is always created with
                              ``proxy_enabled=True``, whatever is passed. The parameter is
                              kept so that existing calls keep working.
        :type proxy_enabled: bool
        :param description: Short description of the provider. Defaults to empty string.
        :type description: str
        :param auth_patterns: Authentication options available to users. Each element
                               must be an AuthPattern instance. Currently only a single
                               AuthPattern is supported — pass a list with exactly one
                               element. The list type is intentional for future
                               multi-pattern support. Required in practice: leaving
                               it out and passing an empty list fail the same way
                               (400 INVALID_ARGUMENT, a validation error on
                               provider.auth_patterns), because an empty list is
                               not sent. The SDK checks neither before sending.
        :type auth_patterns: Optional[List[AuthPattern]]
        :param icon_src: URL of the provider's icon image. Optional.
        :type icon_src: Optional[str]
        :param metadata: Arbitrary string key-value pairs attached to the provider. Optional.
        :type metadata: Optional[Dict[str, str]]
        :param openapi_spec_url: HTTPS URL of an OpenAPI spec (JSON or YAML; a Swagger 2.0
                                 document is converted) to source the connector's tools
                                 from. Must start with 'https://' (at most 2048 characters).
                                 The server fetches it before storing anything and rejects an
                                 unreachable URL or a document that is not a valid OpenAPI or
                                 Swagger spec with 400 INVALID_ARGUMENT (the message starts with
                                 ``openapi_spec_url failed validation``). A spec is limited to
                                 5 MB by default, and to 50 MB together with the files it
                                 references.
        :type openapi_spec_url: Optional[str]

        :returns: Tuple of (CreateProviderResponse proto, grpc.Call).
                  response[0].provider contains the created provider proto. Its
                  ``identifier`` is what update_custom_provider and delete_custom_provider
                  take, and the ``provider`` to pass to
                  ``scalekit_client.actions.create_connection`` to create a connection to
                  the connector.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        # A custom connector is always created with proxy_enabled=True, whatever the caller passes: the
        # parameter is kept only so that existing calls do not break.
        provider = CreateCustomProvider(
            display_name=display_name,
            description=description,
            proxy_enabled=True,
        )
        if proxy_url:
            provider.proxy_url = proxy_url
        if openapi_spec_url:
            provider.openapi_spec_url = openapi_spec_url
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
        proxy_url: Optional[str] = None,
        description: Optional[str] = None,
        auth_patterns: Optional[List[AuthPattern]] = None,
        icon_src: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        openapi_spec_url: Optional[str] = None,
    ):
        """Update an existing custom provider.

        The server applies this as a PUT: it replaces the provider's settings and is not a
        partial update. It requires display_name and auth_patterns on every update, and
        proxy_url as well for an MCP-sourced connector (400 'proxy_url is required for an
        MCP-sourced connector'). Optional fields left as None are not sent: description
        and icon_src then keep their stored values, but metadata is cleared (see that
        parameter).

        The call always sends ``proxy_enabled=True``, which ``create_custom_provider`` always sets,
        and has no parameter for it. The server applies the flag on every update, so an update
        switches proxying on for a connector that has it off (created that way by another client
        such as the dashboard, the REST API or another SDK, or switched off by an
        ``update_custom_provider`` call of an SDK release up to 2.25.0, which sent False). An
        OpenAPI-sourced connector in that state cannot be updated here: the server rejects a value
        that differs from the stored one (see below) with the same 400 as for a locked field.
        ``Provider.proxy_enabled`` from ``list_providers`` shows which connectors are affected.

        An OpenAPI-sourced connector (one created with ``openapi_spec_url``) can only
        change display_name, description, icon_src, metadata and proxy_url, which is its
        base URL, and openapi_spec_url where the workspace has that capability enabled
        (see below). A request that changes anything else is rejected with 400
        INVALID_ARGUMENT ('an OpenAPI-sourced connector can only update metadata,
        display_name, description, icon_src and proxy_url ...'). That covers auth_patterns
        too, but only when their content differs from the stored value, so send them back
        exactly as list_providers returned them. A pattern the SDK
        decoded is sent back as the server returned it, key for key, as long as you have not
        changed it. A pattern you rebuild by hand counts as a change unless it matches the
        stored one exactly, ``is_open_api`` flag and empty values such as ``"hint": ""``
        included.

        Changing the base URL (ignoring a trailing slash) saves it and queues a new tool
        collection run that regenerates every tool. Where OpenAPI-sourced connectors are not
        enabled for the environment, it fails with 400 FEATURE_NOT_ENABLED and nothing is
        saved. If a run is already in progress, the value is still saved but the call fails
        with 409 RESOURCE_ALREADY_EXISTS; call ``scalekit_client.actions.invoke_tool_collection``
        once that run completes. Changing ``openapi_spec_url`` to a different value needs a separate
        capability and fails with 400 FEATURE_NOT_ENABLED ('updating the OpenAPI spec URL of
        an existing connector is not enabled for this workspace') where it is off; where it
        is on, the new URL is validated and every tool is regenerated. Sending the stored
        spec URL again does nothing, and a connector that was not created from a spec cannot
        gain one (400 INVALID_ARGUMENT).

        :param identifier: Identifier of the custom provider to update. Required.
        :type identifier: str
        :param display_name: Name shown in the UI. ASCII letters (a-z, A-Z), digits and
                             spaces only, 1-200 characters, with at least one letter or
                             digit; anything else, such as accented letters or symbols
                             like '_' or '-', is rejected. Changing the name does not
                             change the identifier. Good practice: suffix with 'MCP' for
                             MCP server providers. Required.
        :type display_name: str
        :param proxy_url: HTTPS URL of the external service this provider connects to, and
                          the address Scalekit sends proxied requests to. For an
                          MCP-sourced connector, its server URL (required). For an API
                          connector, the API's base URL. For an OpenAPI-sourced connector,
                          its base URL, which you may omit to keep the stored one. Must
                          start with 'https://'.
        :type proxy_url: Optional[str]
        :param description: New description. Pass None to leave unchanged. An empty
                            string does not clear it: the server ignores empty values.
        :type description: Optional[str]
        :param auth_patterns: The auth patterns. The server requires this on every update:
                               leaving it out (None) is rejected with 400 INVALID_ARGUMENT, a
                               validation error on provider.auth_patterns. When it is a
                               different list, the server replaces the existing one rather
                               than merging. It accepts an empty list and then keeps the
                               stored patterns (the typed UpdateCustomProviderRequest refuses
                               one). To keep the current patterns, send the
                               ones list_providers returned. Currently only a single
                               AuthPattern is supported — pass a list with exactly one
                               element. The list type is intentional for future
                               multi-pattern support. The auth type and the connector
                               kind (MCP or API) cannot be changed, and an API_KEY
                               provider cannot switch between single-key and
                               multiple-headers mode.
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
        :param openapi_spec_url: HTTPS URL of the OpenAPI spec of an OpenAPI-sourced
                                 connector. Leave it out unless you mean to change the spec
                                 source, or send the stored value back for a no-op.
        :type openapi_spec_url: Optional[str]

        :returns: Tuple of (UpdateProviderResponse proto, grpc.Call).
                  response[0].provider contains the updated provider proto.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        # proxy_enabled is a plain bool on the wire: the server applies it on every update and, for an
        # OpenAPI-sourced connector, rejects a value that differs from the stored one. The SDK always
        # creates a connector with True, so send True rather than the proto default (False).
        provider = UpdateCustomProvider(display_name=display_name, proxy_enabled=True)
        if proxy_url is not None:
            provider.proxy_url = proxy_url
        if description is not None:
            provider.description = description
        if auth_patterns is not None:
            provider.auth_patterns.CopyFrom(_patterns_to_list_value(auth_patterns))
        if icon_src is not None:
            provider.icon_src = icon_src
        if metadata is not None:
            provider.metadata.update(metadata)
        if openapi_spec_url is not None:
            provider.openapi_spec_url = openapi_spec_url
        return self.core_client.grpc_exec(
            self._stub.UpdateCustomProvider.with_call,
            UpdateCustomProviderRequest(identifier=identifier, provider=provider),
        )

    def delete_custom_provider(self, identifier: str):
        """Delete a custom provider by identifier.

        Deletion is permanent. The provider is removed from the Scalekit catalog
        and can no longer be used for new connections. It also removes the provider's
        discovered custom MCP tools.

        A connector that still has connections is not deleted: the call raises
        ScalekitBadRequestException (400, PROVIDER_HAS_EXISTING_CONNECTIONS). Remove
        its connected accounts first, then its connections with
        ``scalekit_client.actions.delete_connection`` (a connection that still has
        connected accounts cannot be deleted either), then delete the provider.
        The server checks this before the run described next.

        For a connector created from an OpenAPI spec: while a tool collection run
        of the connector is queued or processing, nothing is deleted: the call
        raises ScalekitConflictException (409, RESOURCE_ALREADY_EXISTS) and the
        message names the run. Poll that run with
        ``scalekit_client.actions.get_tool_collection_run`` (pass its ID as run_id) and
        retry once it has finished; the server fails a run that
        makes no progress after about 30 minutes. An MCP or plain REST connector has
        no run to wait for.

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
                              ProviderType.ALL=2. Pass None to return built-in
                              providers only (same as DEFAULT); use ALL or CUSTOM
                              to include custom providers.
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
