from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.events.events_pb2 import *
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
        self.events_service = EventsServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_events_paginated(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter: Optional[EventFilter] = None,
    ) -> ListEventsPaginatedResponse:
        """
        Method to list events with pagination

        :param page_size   : page size for events list fetch (optional, uses server default if not provided)
        :type              : ``` int ```
        :param page_token  : page token for events list fetch
        :type              : ``` str ```
        :param filter      : EventFilter object to filter events (optional)
        :type              : ``` obj ```

        :returns:
            List Events Paginated Response
        """
        request = ListEventsPaginatedRequest()
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        if filter is not None:
            request.filter.CopyFrom(filter)
        return self.core_client.grpc_exec(
            self.events_service.ListEventsPaginated.with_call,
            request,
        )
