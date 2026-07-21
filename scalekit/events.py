from typing import List, Optional, Union

from scalekit.core import CoreClient
from scalekit.v1.events.events_pb2 import (
    EventFilter,
    ListEventsRequest,
    ListEventsResponse,
    Source,
)
from scalekit.v1.events.events_pb2_grpc import EventsServiceStub


class EventsClient:
    """Class definition for Events Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Events Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.events_service = EventsServiceStub(self.core_client.grpc_secure_channel)

    def list_events(
        self,
        event_types: Optional[List[str]] = None,
        start_time=None,
        end_time=None,
        organization_id: Optional[str] = None,
        source: Optional[Union[str, int]] = None,
        auth_request_id: Optional[str] = None,
        interceptor_id: Optional[str] = None,
        interceptor_status: Optional[str] = None,
        interceptor_decision: Optional[str] = None,
        connection_id: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> ListEventsResponse:
        """
        Method to list events for the current environment, ordered most-recent first.

        :param event_types            : Filter by one or more event type names
        :type                         : ``` List[str] ```
        :param start_time             : Only return events at or after this timestamp
        :type                         : ``` google.protobuf.Timestamp ```
        :param end_time               : Only return events at or before this timestamp
        :type                         : ``` google.protobuf.Timestamp ```
        :param organization_id        : Filter by organization ID
        :type                         : ``` str ```
        :param source                 : Filter by event source ("SCALEKIT" or "DIR_SYNC")
        :type                         : ``` str | int ```
        :param auth_request_id        : Filter by the authentication request that produced the
                                        events. Correlate with a value returned by
                                        AuditLogsClient.list_auth_requests()'s auth_request_id field.
        :type                         : ``` str ```
        :param interceptor_id         : Filter by interceptor ID
        :type                         : ``` str ```
        :param interceptor_status     : Filter by interceptor status
        :type                         : ``` str ```
        :param interceptor_decision   : Filter by interceptor decision
        :type                         : ``` str ```
        :param connection_id          : Filter by connection ID
        :type                         : ``` str ```
        :param connected_account_id   : Filter by connected account ID
        :type                         : ``` str ```
        :param page_size              : Number of events to return per page
        :type                         : ``` int ```
        :param page_token             : Opaque pagination cursor from a previous response
        :type                         : ``` str ```

        :returns:
            List Events Response
        """
        event_filter = EventFilter(
            organization_id=organization_id,
            auth_request_id=auth_request_id,
            interceptor_id=interceptor_id,
            interceptor_status=interceptor_status,
            interceptor_decision=interceptor_decision,
            connection_id=connection_id,
            connected_account_id=connected_account_id,
            start_time=start_time,
            end_time=end_time,
        )
        if event_types:
            event_filter.event_types.extend(event_types)
        if source is not None:
            event_filter.source = (
                Source.Value(source) if isinstance(source, str) else source
            )

        request = ListEventsRequest(
            filter=event_filter,
            page_size=page_size,
            page_token=page_token,
        )
        return self.core_client.grpc_exec(
            self.events_service.ListEvents.with_call, request
        )
