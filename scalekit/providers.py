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
    GetToolCollectionRunRequest,
    ListProvidersRequest,
    TriggerToolCollectionRequest,
)
from scalekit.v1.providers.providers_pb2_grpc import ProviderServiceStub


def _patterns_to_list_value(patterns: List[AuthPattern]) -> struct_pb2.ListValue:
    # The wire form, not to_dict(): a pattern decoded from a response goes back exactly as the
    # server returned it, which an OpenAPI-sourced connector's update needs (see AuthPattern).
    return ParseDict([p._to_wire_dict() for p in patterns], struct_pb2.ListValue())


def _stripped(value):
    """A string without the whitespace around it; anything else (None, a wrong type) is left for the stub to refuse."""
    return value.strip() if isinstance(value, str) else value


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
        get_tool_collection_run(identifier, "latest"). The connector's base URL
        (``proxy_url`` on the returned provider) is filled in from the spec's own server
        URL by that run, only when that URL starts with https:// (otherwise it stays empty).
        Set or change it with update_custom_provider.

        Errors surface as ScalekitServerException subclasses: 400 INVALID_ARGUMENT for
        an invalid request, 400 FEATURE_NOT_ENABLED when OpenAPI-sourced connectors are
        not enabled for the environment, and 409 RESOURCE_ALREADY_EXISTS when an
        OpenAPI connector with the same name already exists in the environment.

        With ``openapi_spec_url`` the call is not retried automatically when the service
        is unavailable (an HTTP 429 from the edge is not retried either: it never reached Scalekit, so repeating the call is safe): the create is not idempotent, and if the first attempt created the
        connector but its response was lost, a retry would fail with
        ScalekitConflictException although the connector exists. After such a
        ScalekitServiceUnavailableException, look the connector up with list_providers
        (provider_type=ProviderType.CUSTOM, following next_page_token: the default lists
        built-in providers only) before you create it again. The same goes for a
        ScalekitGatewayTimeoutException (the client's tool-call timeout passed, and the call
        does not retry it): the server may have finished the create. An MCP-sourced create
        keeps the default retry.

        :param display_name: Human-readable name for the provider. Required.
                             Accepted characters: a-z, A-Z, 0-9, and spaces.
                             Good practice: suffix with 'MCP' for MCP server providers.
        :type display_name: str
        :param proxy_url: HTTPS URL of the MCP server for an MCP-sourced connector. Must
                          start with 'https://' (at most 2048 characters). Leave it out when
                          you pass ``openapi_spec_url``: the server rejects both together.
        :type proxy_url: Optional[str]
        :param proxy_enabled: Ignored. A custom connector is always created with
                              ``proxy_enabled=True``, whatever is passed. The parameter is
                              kept so that existing calls keep working.
        :type proxy_enabled: bool
        :param description: Short description of the provider. Defaults to empty string.
        :type description: str
        :param auth_patterns: Authentication options available to users. Each element
                               must be an AuthPattern instance. The server requires at
                               least one pattern and rejects a request without one.
                               Currently only a single AuthPattern is supported — pass a
                               list with exactly one element. The list type is intentional
                               for future multi-pattern support.
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
                  response[0].provider contains the created provider proto.
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
            # With a spec URL the server fetches the spec while it answers, which can take
            # longer than an ordinary control-plane call.
            timeout=self.core_client.tool_call_timeout_s if openapi_spec_url else None,
            # The first attempt may already have created the connector, and a retry would then
            # hit the duplicate-name check of OpenAPI connectors (409) instead of succeeding.
            retry_on_unavailable=not openapi_spec_url,
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

        The server requires display_name and auth_patterns on every update, and
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
        with 409 RESOURCE_ALREADY_EXISTS; call trigger_tool_collection once that run
        completes. Changing ``openapi_spec_url`` to a different value needs a separate
        capability and fails with 400 FEATURE_NOT_ENABLED ('updating the OpenAPI spec URL of
        an existing connector is not enabled for this workspace') where it is off; where it
        is on, the new URL is validated and every tool is regenerated. Sending the stored
        spec URL again does nothing, and a connector that was not created from a spec cannot
        gain one (400 INVALID_ARGUMENT).

        With ``openapi_spec_url`` the call is not retried automatically when the service is
        unavailable (an HTTP 429 from the edge is not retried either: it never reached Scalekit, so repeating the call is safe): the first attempt may already have saved the new URL, and a repeat finds
        nothing to change, so it queues no run and still succeeds. After such a
        ScalekitServiceUnavailableException, read the connector back with list_providers. If
        its openapi_spec_url is the new value, wait for any active run to finish and call
        trigger_tool_collection; otherwise send the update again. A
        ScalekitGatewayTimeoutException is not retried either, and the server may have
        finished: check the same way before you repeat the call. An update without
        ``openapi_spec_url`` keeps the default retry, including one that changes the base URL
        (``proxy_url``) of an OpenAPI-sourced connector: that change queues a run too, and a
        repeat after a lost answer finds nothing to change and queues none. After such an
        update, check get_tool_collection_run(identifier, "latest") and call
        trigger_tool_collection if no new run appeared (the SDK cannot tell an OpenAPI-sourced
        connector from an MCP one here, so the retry stays for both).

        :param identifier: Identifier of the custom provider to update. Required.
        :type identifier: str
        :param display_name: Display name for the provider. Accepted characters:
                             a-z, A-Z, 0-9, and spaces. Good practice: suffix with
                             'MCP' for MCP server providers. Required.
        :type display_name: str
        :param proxy_url: For an MCP-sourced connector, its HTTPS server URL (required).
                          For an OpenAPI-sourced connector, its base URL, which you may
                          omit to keep the stored one. Must start with 'https://'.
        :type proxy_url: Optional[str]
        :param description: New description. Pass None to leave unchanged.
        :type description: Optional[str]
        :param auth_patterns: The auth patterns. The server requires this on every update
                               and, when it is a different list, replaces the existing one
                               rather than merging. To keep the current patterns, send the
                               ones list_providers returned. Currently only a single
                               AuthPattern is supported — pass a list with exactly one
                               element. The list type is intentional for future
                               multi-pattern support.
        :type auth_patterns: Optional[List[AuthPattern]]
        :param icon_src: New icon URL. Pass None to leave unchanged.
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
            # A different spec URL is fetched while the server answers (see create_custom_provider).
            timeout=self.core_client.tool_call_timeout_s if openapi_spec_url else None,
            # The first attempt may already have saved the new URL without queueing its run, and a
            # repeat finds nothing to change: it would succeed and queue none.
            retry_on_unavailable=not openapi_spec_url,
        )

    def delete_custom_provider(self, identifier: str):
        """Delete a custom provider by identifier.

        Deletion is permanent. The provider is removed from the Scalekit catalog
        and can no longer be used for new connections.

        A connector that still has connections is not deleted: the call raises
        ScalekitBadRequestException (400, PROVIDER_HAS_EXISTING_CONNECTIONS); delete its
        connections first. The server checks this before the run described next.

        For a connector created from an OpenAPI spec: while a tool collection run
        of the connector is queued or processing, nothing is deleted: the call
        raises ScalekitConflictException (409, RESOURCE_ALREADY_EXISTS) and the
        message names the run. Poll that run with get_tool_collection_run (pass its
        ID as run_id) and retry once it has finished; the server fails a run that
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

    def trigger_tool_collection(self, provider_identifier: str):
        """Queue a new tool collection run on an OpenAPI-sourced connector.

        The server re-fetches and validates the connector's current spec URL, queues an
        asynchronous run against it, and returns that run at once with status QUEUED. The
        run regenerates the connector's tools: new operations become tools, changed ones are
        refreshed, and tools whose operation left the spec are deleted. Follow the run with
        get_tool_collection_run.

        A connector is also re-synced automatically when it is created and when its base URL
        or spec URL changes, so you call this to pick up changes to the spec itself or to
        retry after a failed run. If the spec, base URL and auth patterns have not changed
        since the last completed run, the new run completes without creating, updating or
        deleting anything (the server does not take that shortcut for a spec that
        references external files). If the first run fills in the base URL (only when the
        spec's server URL starts with https://) or the OAuth settings, the next run still
        updates every tool and the shortcut applies from the run after that; otherwise the
        shortcut already applies to the second run.

        The call is not retried automatically when the service is unavailable, because the
        first attempt may already have queued a run (an HTTP 429 from the edge is not retried either: it never reached Scalekit, so repeating the call is safe). As for create_custom_provider, the server
        fetches the spec while it answers, so the call uses the client's tool-call timeout.
        After a ScalekitServiceUnavailableException or a ScalekitGatewayTimeoutException,
        check get_tool_collection_run(identifier, "latest") before you trigger again: the
        first attempt may already have queued the run, and a second trigger while it is
        active answers 409.

        Errors surface as ScalekitServerException subclasses: ScalekitNotFoundException
        (404) when no such connector exists in the environment; ScalekitBadRequestException
        (400) when the connector is not sourced from an OpenAPI spec ('this connector is not
        sourced from an OpenAPI spec'), when the stored spec URL fails validation
        ('openapi_spec_url failed validation: ...'), or when OpenAPI-sourced connectors are
        not enabled for the environment (FEATURE_NOT_ENABLED); and
        ScalekitConflictException (409 RESOURCE_ALREADY_EXISTS, 'an ingestion run is already
        in progress for this connector') when a run is queued or running, because a connector
        has at most one active run.

        :param provider_identifier: Identifier of the OpenAPI-sourced connector. Required.
        :type provider_identifier: str

        :returns: Tuple of (ToolCollectionRun proto, grpc.Call).
                  response[0] is the queued run.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        return self.core_client.grpc_exec(
            self._stub.TriggerToolCollection.with_call,
            TriggerToolCollectionRequest(provider_identifier=_stripped(provider_identifier)),
            timeout=self.core_client.tool_call_timeout_s,
            retry_on_unavailable=False,
        )

    def get_tool_collection_run(self, provider_identifier: str, run_id: str = "latest"):
        """Read one tool collection run of an OpenAPI-sourced connector.

        Returns the run's status, its counters (operations found, tools created, updated and
        deleted) and, once the run has finished, the operations it skipped and why.

        A run moves QUEUED, PROCESSING, then COMPLETED or FAILED. The server marks a run
        that makes no progress for 30 minutes FAILED. A run fails when the spec cannot be
        fetched or parsed, when none of its operations can be converted into a tool, or when
        it takes too long; error_message says which. Operations that cannot become tools are
        skipped and reported instead (for example a request body that is not JSON or
        form-encoded, an operation that needs authentication when no auth pattern is
        configured, or an HTTP method other than GET, POST, PUT, PATCH and DELETE) and do
        not fail the run.

        Errors surface as ScalekitServerException subclasses: ScalekitNotFoundException (404)
        when the connector does not exist, when it has no run yet, or when run_id names no
        run of this connector ('tool collection run not found'); and
        ScalekitBadRequestException (400, 'invalid run_id') when run_id is not a valid run ID.

        :param provider_identifier: Identifier of the connector the run belongs to. Required.
        :type provider_identifier: str
        :param run_id: A run ID, or "latest" (the default; an empty or blank string means the
                       same) for the connector's most recent run.
        :type run_id: str

        :returns: Tuple of (ToolCollectionRun proto, grpc.Call).
                  response[0] is the run.
                  response[1].code().name == 'OK' on success.
        :rtype: tuple
        """
        return self.core_client.grpc_exec(
            self._stub.GetToolCollectionRun.with_call,
            GetToolCollectionRunRequest(
                provider_identifier=_stripped(provider_identifier), run_id=_stripped(run_id) or "latest"
            ),
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
                           Pass None to return all providers.
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
