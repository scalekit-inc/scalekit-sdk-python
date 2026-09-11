from typing import TypeVar, Optional, Protocol

import math
import random
import time
from http import HTTPStatus

import grpc
import jwt
import json
import requests
import platform
from urllib.parse import urlparse
from requests.models import Response

from cryptography.hazmat.primitives import serialization
from scalekit._version import __version__ as _sdk_version
from scalekit.common.scalekit import GrantType
from scalekit.common.exceptions import ScalekitServerException, ScalekitException, ScalekitTooManyRequestsException

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TMetadata = TypeVar("TMetadata")

TOKEN_ENDPOINT = "/oauth/token"
JWKS_ENDPOINT = "/keys"

# Must clear the backend's EnforcementPolicy.MinTime (30s, scalekit's
# cmd/grpc.go) with real margin, not just match it: grpc-core pings on this
# exact interval for as long as the channel is open (keepalive_permit_without_calls
# below), so a value equal to MinTime leaves zero room for jitter between the
# client's timer and the server's strike window — one early ping is a strike,
# three and the server GOAWAYs the connection, recreating the bug this fixes.
# 60s matches the Java SDK's default for the same reason.
DEFAULT_KEEPALIVE_TIME_MS = 60_000
DEFAULT_KEEPALIVE_TIMEOUT_MS = 10_000

# The floor tracks DEFAULT_KEEPALIVE_TIME_MS for the reason spelled out above:
# the backend's EnforcementPolicy.MinTime is 30s, and a value at exactly 30s has
# zero jitter headroom — grpc's ping timer drifts slightly early, so an early
# ping counts as a strike and enough strikes make the server GOAWAY. 60s gives
# 2x margin over the 30s MinTime. Since there is no legitimate reason to go below
# the default, the only sensible choices are 0 (disabled) or >= 60s. (gRPC also
# silently clamps sub-10s values up to 10s per grpc/proposal A8, so a small value
# never even reaches the wire as requested.) Reject 1..59999.
MIN_KEEPALIVE_TIME_MS = 60_000

# grpc-core exposes 'grpc.client_idle_timeout_ms' (gRFC A9) as the client-side
# equivalent of what the Go and Node SDKs implement by hand on their
# self-managed HTTP/2 transports (grpcIdleConnTimeout / idleConnectionTimeoutMs):
# proactively transition a fully-idle channel so its connection is torn down
# and lazily recreated on the next call, instead of waiting to discover it's
# dead (or waiting for the backend to GOAWAY it) only when a real request is
# written to it. This SDK previously configured keepalive pings but never this
# option — the gap this constant and CLIENT_IDLE_TIMEOUT_PING_CYCLES close.
#
# Must stay strictly BELOW the backend's own grpcKeepaliveMaxConnectionIdle
# (5 min, scalekit's cmd/grpc.go), not equal to it: landing exactly on the
# backend's bound is a race — whichever side's timer fires first wins, and the
# loser is a request written into a socket the other side just closed. Mirrors
# the Go SDK's grpcIdleConnCeiling and the Node SDK's
# IDLE_CONNECTION_TIMEOUT_CEILING_MS exactly (both 4 minutes), for the same
# reason.
CLIENT_IDLE_TIMEOUT_CEILING_MS = 240_000

# Multiplier applied to keepalive_time_ms before clamping to the ceiling above
# — mirrors the Go SDK's grpcIdleConnPingCycles / Node SDK's
# IDLE_PING_CYCLES_BEFORE_CLOSE (both 5) exactly, so this SDK scales down
# correctly alongside the other two should MIN_KEEPALIVE_TIME_MS itself ever
# be lowered. Superseded by the ceiling for every currently-valid non-zero
# keepalive_time_ms (60s x 5 = 300s already exceeds the 4-minute ceiling).
CLIENT_IDLE_TIMEOUT_PING_CYCLES = 5

# requests defaults to no timeout, so a black-holed connection blocks the
# calling thread until the OS abandons the socket. Bound the connect and read
# phases separately with a (connect, read) tuple.
DEFAULT_HTTP_CONNECT_TIMEOUT_S = 10
DEFAULT_HTTP_READ_TIMEOUT_S = 30
DEFAULT_HTTP_TIMEOUT = (DEFAULT_HTTP_CONNECT_TIMEOUT_S, DEFAULT_HTTP_READ_TIMEOUT_S)

# grpc-python stub calls default timeout=None (no deadline) when the caller
# doesn't pass one — grpc_exec never did, so a call could block forever on a
# connection the keepalive check above hasn't (yet) noticed is dead, exactly
# the same class of bug the HTTP timeout above exists to prevent. Matches the
# Node SDK's timeoutMs default (20s) for the same control-plane calls.
#
# This bounds each individual attempt, not the total call: grpc_exec passes
# the same value into every retry recursion (see UNAVAILABLE's backoff retry
# below), so a call that retries takes up to (retries + 1) x this value in
# the worst case, not this value total. A monotonic total-budget deadline
# (compute once, pass the remaining time per attempt) would close that gap
# but isn't implemented — left as a known, documented gap rather than a
# silent one.
DEFAULT_CALL_TIMEOUT_S = 20

# Tool execution (ToolsClient) proxies to third-party APIs (Gmail, Slack, ...)
# whose own latency this SDK doesn't control, so it gets a longer deadline
# than ordinary control-plane calls. Deliberately kept BELOW the infra load
# balancer's backend timeout for this path (62s, per infra config), rather
# than matching it: two independent timers racing at the identical value
# produce a coin-flip on which one fires first, and a caller sees two
# different failure signatures (a clean ScalekitGatewayTimeoutException vs
# whatever shape the LB's own forced termination takes) for the same
# underlying "this call ran too long" condition. Landing below the LB's
# bound makes the SDK's own deadline the deterministic, always-first
# timeout, so callers always get the same, well-formed exception.
DEFAULT_TOOL_CALL_TIMEOUT_S = 60

# Backoff for the retry_on_unavailable path (UNAVAILABLE only — see grpc_exec).
# The backoff FORMULA matches the Node SDK's exactly: base doubles each
# attempt up to a 30s ceiling, then half-jittered (0.5-1.0x) so a fleet of
# clients retrying the same overloaded backend doesn't retry in lockstep.
# This is only agreement on the formula, not on runtime behavior for the
# failure mode that matters most — see the UNAVAILABLE branch in grpc_exec
# for why a transport reset still reaches this retry in Python but not in
# Node, despite both naming the retried code UNAVAILABLE/Unavailable. Does
# not apply to the UNAUTHENTICATED retry (immediate — a 401 isn't a signal
# the backend is under load).
RETRY_BACKOFF_BASE_S = 1.0
RETRY_BACKOFF_MAX_S = 30.0


def _assert_valid_timeout(name: str, value) -> None:
    """A non-positive or non-finite timeout is never what the caller wants:
    grpc-python treats timeout=0/negative as "already expired" (the call fails
    immediately) and this SDK has no "no deadline" escape hatch — silently
    reintroducing the unbounded-block bug this parameter exists to fix is not
    an option worth offering. Shared by the constructor (call_timeout_s/
    tool_call_timeout_s) and grpc_exec's per-call override, so an override
    can't bypass the same rule."""
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(
            f"{name} must be a positive, finite number of seconds; got {value!r}."
        )


def _client_idle_timeout_ms_for(keepalive_time_ms: int) -> int:
    """Derive grpc.client_idle_timeout_ms from keepalive_time_ms — mirrors the
    Go SDK's idleConnTimeoutFor / Node SDK's idleConnectionTimeoutMsFor exactly
    (same formula, same constants), so the three SDKs land on the same idle-close
    behavior. keepalive_time_ms == 0 (disabled) returns 0, meaning "not set" to
    the caller (see __grpc_secure_channel — no option is passed, so grpc-core's
    own much larger default applies), consistent with keepalive_time_ms == 0
    disabling the ping-based idle detection above too."""
    if not keepalive_time_ms:
        return 0
    scaled = keepalive_time_ms * CLIENT_IDLE_TIMEOUT_PING_CYCLES
    if scaled <= 0 or scaled > CLIENT_IDLE_TIMEOUT_CEILING_MS:
        return CLIENT_IDLE_TIMEOUT_CEILING_MS
    return scaled


def _is_success_status(status_code: int) -> bool:
    """200-only would be a footgun: the token/JWKS endpoints are only ever
    expected to reply 200, but a strict != 200 check would misclassify any
    other legitimate 2xx (e.g. 201/202/204) as an error. Check the actual
    success range instead of hardcoding a single code."""
    return 200 <= status_code < 300


def _as_gateway_timeout_response(exp: Exception) -> Response:
    """Wrap a requests timeout as a synthetic 504 Response so it flows through
    ScalekitServerException.promote() like any other HTTP error, instead of
    leaking a raw requests exception past the SDK's exception boundary —
    matches the Node SDK's ScalekitGatewayTimeoutException.fromAxiosTimeout."""
    response = Response()
    response.status_code = HTTPStatus.GATEWAY_TIMEOUT
    response.reason = "GATEWAY_TIMEOUT"
    response.encoding = "utf-8"
    response._content = str(exp).encode("utf-8")
    return response


class WithCall(Protocol):
    # timeout: Optional to match grpc's multicallables (e.g. UnaryUnaryMultiCallable.with_call),
    # which themselves default it to None rather than requiring it.
    def __call__(self, request: TRequest, timeout: Optional[float] = None, metadata: TMetadata = None) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = f"Scalekit-Python/{_sdk_version}"
    # YYYYMMDD
    api_version = "20260909"
    user_agent = f"{sdk_version} Python/{platform.python_version()} ({platform.system()}; {platform.architecture()}"

    def __init__(
        self,
        env_url,
        client_id,
        client_secret,
        keepalive_time_ms: int = DEFAULT_KEEPALIVE_TIME_MS,
        keepalive_timeout_ms: int = DEFAULT_KEEPALIVE_TIMEOUT_MS,
        call_timeout_s: float = DEFAULT_CALL_TIMEOUT_S,
        tool_call_timeout_s: float = DEFAULT_TOOL_CALL_TIMEOUT_S,
    ):
        """
        Initializer for Core client

        :param env_url               : Environment URL
        :type                        : ``` str ```
        :param client_id             : Client ID
        :type                        : ``` str ```
        :param client_secret         : Client Secret
        :type                        : ``` str ```
        :param keepalive_time_ms     : How often, in milliseconds, an idle gRPC
                                        connection is verified before reuse.
                                        Must stay above the backend's keepalive
                                        MinTime (30s) with real margin, or the
                                        server treats this ping as abuse. Also
                                        derives grpc.client_idle_timeout_ms (see
                                        CLIENT_IDLE_TIMEOUT_CEILING_MS), which
                                        proactively recycles a connection with
                                        zero active calls before the backend's
                                        own MaxConnectionIdle would. Defaults to
                                        60000. Set to 0 to disable both of this
                                        SDK's own settings for these — grpc-core
                                        still applies its own (much larger)
                                        default idle behavior when no options
                                        are passed at all, so this isn't "no
                                        idle handling," just no SDK-configured one.
        :type                        : ``` int ```
        :param keepalive_timeout_ms  : How long, in milliseconds, to wait for a
                                        keepalive response before treating an
                                        idle connection as dead. Defaults to
                                        10000.
        :type                        : ``` int ```
        :param call_timeout_s        : Deadline, in seconds, applied to every gRPC
                                        call unless a call site overrides it (e.g.
                                        tool execution — see tool_call_timeout_s).
                                        Without this, a call can block forever on
                                        a connection that looks fine to the client
                                        but is silently dead. Defaults to 20.
        :type                        : ``` float ```
        :param tool_call_timeout_s   : Deadline, in seconds, for tool-execution
                                        calls (ToolsClient), which proxy to
                                        third-party APIs and can legitimately run
                                        longer than ordinary control-plane calls.
                                        Defaults to 60, deliberately below the
                                        infra load balancer's 62s backend timeout
                                        for this path so this deadline is always
                                        the one that fires, not a coin flip.
        :type                        : ``` float ```
        :returns
            None
        """
        parsed_url = urlparse(env_url)
        self.host = parsed_url.netloc
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret
        # 0 means "disabled" and is allowed through deliberately; only 1..59999
        # is rejected. A value below the 60s default leaves too little margin
        # over the Scalekit server's 30s MinTime — an early ping gets struck as
        # abusive and the server GOAWAYs — and gRPC silently raises sub-10s
        # values to 10s, so a small value is never what the caller asked for.
        if keepalive_time_ms and keepalive_time_ms < MIN_KEEPALIVE_TIME_MS:
            raise ValueError(
                f"keepalive_time_ms must be 0 (disabled) or >= {MIN_KEEPALIVE_TIME_MS}; "
                f"got {keepalive_time_ms}. A value below the default leaves too little "
                "margin over the Scalekit server's 30s MinTime (early pings are struck "
                "as abusive), and gRPC silently raises sub-10s values to 10s."
            )
        _assert_valid_timeout("call_timeout_s", call_timeout_s)
        _assert_valid_timeout("tool_call_timeout_s", tool_call_timeout_s)
        self.keepalive_time_ms = keepalive_time_ms
        self.keepalive_timeout_ms = keepalive_timeout_ms
        self.call_timeout_s = call_timeout_s
        self.tool_call_timeout_s = tool_call_timeout_s
        self.keys = {}
        self.access_token = None
        self.grpc_secure_channel = None
        self.__authenticate_client()
        self.__grpc_secure_channel()

    def __grpc_secure_channel(self):
        """
        Method to authenticate grpc and create secure grpc channel
        :params
            None
        :returns
            None
        """
        channel_credentials = grpc.ssl_channel_credentials()
        call_credentials = grpc.access_token_call_credentials(self.access_token)
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        )
        # keepalive_time_ms == 0 disables keepalive (and, below, the derived
        # idle-close timeout) entirely: no options are passed, so grpc-core
        # falls back to its own defaults (no idle pings, ~30 min idle timeout)
        # — an escape hatch for a network path that rejects this pattern.
        channel_options = []
        if self.keepalive_time_ms:
            # keepalive_permit_without_calls=1 so an idle channel is still
            # periodically verified: without it, grpc-core only sends HTTP/2
            # keepalive PINGs while there are active calls, so a connection
            # silently dropped by a network intermediary while idle isn't
            # detected until the next real call is written to it.
            channel_options = [
                ('grpc.keepalive_time_ms', self.keepalive_time_ms),
                ('grpc.keepalive_timeout_ms', self.keepalive_timeout_ms),
                ('grpc.keepalive_permit_without_calls', 1),
                ('grpc.http2.max_pings_without_data', 0),
                # Proactively idle out (and lazily recreate on next use) a
                # connection with zero active calls before the backend's own
                # MaxConnectionIdle would — see CLIENT_IDLE_TIMEOUT_CEILING_MS.
                ('grpc.client_idle_timeout_ms', _client_idle_timeout_ms_for(self.keepalive_time_ms)),
            ]
        self.grpc_secure_channel = grpc.secure_channel(
            self.host, composite_credentials, options=channel_options
        )

    def __authenticate_client(self):
        """
        Method to authenticate client  and return access token

        :returns
            access_token
        """
        params = {
            "grant_type": GrantType.ClientCredentials.value,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self.authenticate(data=params)
        if not _is_success_status(response.status_code):
            raise ScalekitServerException.promote(response)
        response = json.loads(response.content)
        self.access_token = response["access_token"]

    def authenticate(self, data: dict):
        """
        Method to execute post request for authentication with given user params

        :param data : params for authentication request
        :type       : ``` str ```
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(
                self.env_url + TOKEN_ENDPOINT,
                headers=self.get_headers(headers=headers),
                data=data,
                verify=True,
                timeout=DEFAULT_HTTP_TIMEOUT,
            )
        except requests.exceptions.Timeout as exp:
            raise ScalekitServerException.promote(_as_gateway_timeout_response(exp))
        except requests.exceptions.RequestException as exp:
            raise ScalekitException(exp)
        if not _is_success_status(response.status_code):
            raise ScalekitServerException.promote(response)
        return response

    def get_jwks(self):
        """Method to get JWT Keys"""
        if self.keys and len(self.keys) > 0:
            return
        try:
            response = requests.get(
                self.env_url + JWKS_ENDPOINT,
                headers=self.get_headers(),
                timeout=DEFAULT_HTTP_TIMEOUT,
            )
        except requests.exceptions.Timeout as exp:
            raise ScalekitServerException.promote(_as_gateway_timeout_response(exp))
        except requests.exceptions.RequestException as exp:
            raise ScalekitException(exp)
        if not _is_success_status(response.status_code):
            raise ScalekitServerException.promote(response)
        response = json.loads(response.content)
        keys = response["keys"]

        for key in keys:
            kid = key["kid"]
            rsa_key = jwt.PyJWK.from_dict(key).key

            pem_key = rsa_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            self.keys[kid] = pem_key.decode("utf-8")

    def get_headers(self, headers: Optional[dict] = None) -> dict:
        """
        Method to get user defined headers and returns collated header params

        :param headers : User defined header dictionary
        :type          : ``` dict ```
        :returns
            dict
        """
        default_headers = {
            "user-agent": f"{self.user_agent}",
            "x-api-version": f"{self.api_version}",
            "x-sdk-version": f"{self.sdk_version}",
        }
        if self.access_token:
            default_headers.update({"authorization": f"Bearer {self.access_token}"})
        if headers:
            return {**default_headers, **headers}
        return default_headers

    def grpc_exec(
        self,
        func: WithCall,
        data: TRequest,
        retry=2,
        timeout: Optional[float] = None,
        retry_on_unavailable: bool = True,
        _attempt: int = 0,
    ) -> TResponse:
        """
        :param timeout : Per-call deadline override, in seconds. Defaults to
                          ``self.call_timeout_s`` when omitted — pass this
                          explicitly only when a specific call needs a
                          different bound (see ToolsClient's use of
                          ``self.core_client.tool_call_timeout_s``). Validated
                          against the same rule as the constructor's
                          call_timeout_s/tool_call_timeout_s, since grpc_exec
                          is a public method a caller could invoke directly
                          with an unvalidated override. Bounds each attempt
                          individually, not the total call across retries —
                          see DEFAULT_CALL_TIMEOUT_S's comment.
        :type           : ``` Optional[float] ```
        :param retry_on_unavailable : Whether UNAVAILABLE is retried, with
                          backoff, or surfaces immediately. Defaults to True.
                          Note this is a NARROWING of the released SDK's
                          behavior, not a preservation of it — the released
                          SDK retries every status code not already
                          special-cased above (INVALID_ARGUMENT, NOT_FOUND,
                          ALREADY_EXISTS, PERMISSION_DENIED, all of it),
                          immediately, no backoff. Set False at a call site
                          where even the UNAVAILABLE retry risks
                          double-executing a non-idempotent operation (see
                          ToolsClient.execute_tool). Does not affect the
                          separate UNAUTHENTICATED retry below, which is
                          always safe — rejected before touching business
                          logic — regardless of this flag. Also does not
                          affect DEADLINE_EXCEEDED, ABORTED, or INTERNAL/
                          CANCELLED, none of which retry under either value
                          — see the branches below for why each is excluded.
                          When True, a retry sleeps (blocking) for the
                          backoff delay before re-attempting — see
                          RETRY_BACKOFF_BASE_S/RETRY_BACKOFF_MAX_S. Callers
                          holding a lock or a request-handling thread across
                          this call should account for that.
        :type           : ``` bool ```
        :param _attempt : Internal — how many UNAVAILABLE retries have
                          already happened, used to compute the backoff
                          delay before the next one. Not meant to be passed
                          by callers directly. Does not increment on the
                          UNAUTHENTICATED retry, which has no backoff.
        :type           : ``` int ```
        """
        if timeout is None:
            timeout = self.call_timeout_s
        else:
            _assert_valid_timeout("timeout", timeout)
        try:
            resp = func(
                data,
                timeout=timeout,
                metadata=tuple(self.get_headers().items()),
            )
            return resp
        except grpc.RpcError as exp:
            # Check for upstream provider errors first — never retry, never refresh M2M
            error_code = ScalekitServerException._extract_error_code(exp)
            if error_code == "TOOL_ERROR":
                raise ScalekitServerException.promote(exp)

            if exp.code() == grpc.StatusCode.UNAUTHENTICATED:
                if retry <= 0:
                    raise ScalekitServerException.promote(exp)
                # Only a failure of the refresh itself falls back to the original
                # 401 — the retried call's own outcome (success or a different
                # error entirely, e.g. DEADLINE_EXCEEDED) must propagate as-is,
                # not get reported as "unauthorized" just because that's what
                # triggered the first attempt.
                try:
                    self.__authenticate_client()
                except Exception:
                    raise ScalekitServerException.promote(exp)
                return self.grpc_exec(
                    func, data, retry=retry - 1, timeout=timeout,
                    retry_on_unavailable=retry_on_unavailable, _attempt=_attempt,
                )
            elif exp.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                # Surface Scalekit rate-limits immediately — retrying triples the damage
                raise ScalekitServerException.promote(exp)
            elif exp.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                # grpc_exec passes the same `timeout` value into every retry
                # recursion — it bounds each individual attempt, not the total
                # call. Retrying a DEADLINE_EXCEEDED with a fresh full-length
                # window multiplies the worst-case wall-clock time by
                # (retry + 1) instead of bounding it, defeating the point of
                # having a deadline at all (e.g. retry=2 at the 20s
                # call_timeout_s default: 3 x 20s = 60s worst case). A deadline
                # that already expired once retrying it unconditionally makes
                # things worse, not more resilient — so it never retries,
                # regardless of retry_on_unavailable.
                raise ScalekitServerException.promote(exp)
            elif exp.code() == grpc.StatusCode.UNAVAILABLE and retry_on_unavailable and retry > 0:
                # UNAVAILABLE can mean the request already reached and was
                # processed by the server — a dead/refused connection, a stream
                # torn down mid-flight, or a keepalive ping timeout on a
                # still-in-progress call are all indistinguishable to the caller
                # from "the server did the work but the response never made it
                # back." Retrying risks double-executing a non-idempotent call
                # (e.g. execute_tool sending an email). Individual call sites can
                # opt out via retry_on_unavailable=False where double-execution is
                # a real concern — see ToolsClient.execute_tool for the first one.
                #
                # This is NOT "matching this SDK's currently-released behavior":
                # the released SDK's else-branch (`elif retry > 0:`) re-sends on
                # every status code the branches above don't special-case —
                # INVALID_ARGUMENT, NOT_FOUND, ALREADY_EXISTS, PERMISSION_DENIED,
                # all of it, immediately, no backoff. Narrowing the retried set
                # down to UNAVAILABLE alone is the largest user-visible behavior
                # change in this release, not a preserved default — see the PR
                # description for the plain statement of that change.
                #
                # Nor is this full retry-scope parity with the Node SDK, despite
                # both retrying a code spelled UNAVAILABLE/Unavailable: grpc-python
                # classifies a dead/reset connection as UNAVAILABLE natively, so
                # THIS branch fires for exactly the failure mode this ticket
                # (SK-1867) exists to fix. connect-node's own error mapping
                # surfaces that same reset as Code.Aborted, and its retry check
                # (`error.code === Code.Unavailable`, core.ts) runs on that raw
                # code BEFORE the Aborted -> Unavailable re-keying in promote()
                # (base-exception.ts, only reached on the no-retry path) — so
                # Node's Unavailable branch never actually fires for a transport
                # reset; the re-key only affects which exception CLASS the
                # caller sees afterward. The two SDKs agree on the branch's name,
                # not on which real failures reach it.
                #
                # Backed off (jittered exponential, matching the Node SDK's
                # formula) rather than retried immediately: on a backend
                # returning UNAVAILABLE because it's overloaded, every client
                # retrying instantly just triples the load it's already
                # struggling with.
                base_backoff = min(RETRY_BACKOFF_BASE_S * (2 ** _attempt), RETRY_BACKOFF_MAX_S)
                time.sleep(base_backoff * (0.5 + random.random() * 0.5))
                return self.grpc_exec(
                    func, data, retry=retry - 1, timeout=timeout,
                    retry_on_unavailable=retry_on_unavailable, _attempt=_attempt + 1,
                )
            else:
                # ABORTED, INTERNAL, CANCELLED (never retried, any value of
                # retry_on_unavailable) — or UNAVAILABLE when retry_on_unavailable=
                # False (see ToolsClient.execute_tool) or retry is exhausted.
                raise ScalekitServerException.promote(exp)
        except Exception as exp:
            raise ScalekitException(exp)
