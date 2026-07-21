from typing import List, Optional

from scalekit.core import CoreClient
from scalekit.v1.auditlogs.auditlogs_pb2 import (
    ListAuthLogRequest,
    ListAuthLogResponse,
)
from scalekit.v1.auditlogs.auditlogs_pb2_grpc import AuditLogsServiceStub


class AuditLogsClient:
    """Class definition for Audit Logs Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Audit Logs Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.audit_logs_service = AuditLogsServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_auth_requests(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[List[str]] = None,
        start_time=None,
        end_time=None,
        resource_id: Optional[str] = None,
        connected_account_identifier: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> ListAuthLogResponse:
        """
        Method to list authentication request logs for the current environment, ordered
        most-recent first.

        :param page_size                     : Number of authentication request logs to
                                                return per page
        :type                                 : ``` int ```
        :param page_token                     : Opaque pagination cursor from a previous
                                                response
        :type                                 : ``` str ```
        :param email                          : Filter by the end user's email address
        :type                                 : ``` str ```
        :param status                         : Filter by one or more outcome statuses
                                                (e.g. "SUCCESS", "FAILED")
        :type                                 : ``` List[str] ```
        :param start_time                     : Only return authentication logs at or after
                                                this timestamp
        :type                                 : ``` google.protobuf.Timestamp ```
        :param end_time                       : Only return authentication logs at or before
                                                this timestamp
        :type                                 : ``` google.protobuf.Timestamp ```
        :param resource_id                    : Filter by resource ID
        :type                                 : ``` str ```
        :param connected_account_identifier   : Filter by connected account identifier
        :type                                 : ``` str ```
        :param client_id                      : Filter by client ID
        :type                                 : ``` str ```

        :returns:
            List Auth Log Response. Each entry's auth_request_id can be passed to
            EventsClient.list_events(auth_request_id=...) to see every event a specific
            login produced.
        """
        request = ListAuthLogRequest(
            page_size=page_size,
            page_token=page_token,
            email=email,
            start_time=start_time,
            end_time=end_time,
            resource_id=resource_id,
            connected_account_identifier=connected_account_identifier,
            client_id=client_id,
        )
        if status:
            request.status.extend(status)
        return self.core_client.grpc_exec(
            self.audit_logs_service.ListAuthRequests.with_call, request
        )
