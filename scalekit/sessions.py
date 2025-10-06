from scalekit.core import CoreClient
from scalekit.v1.sessions.sessions_pb2 import *
from scalekit.v1.sessions.sessions_pb2_grpc import SessionServiceStub
from google.protobuf.timestamp_pb2 import Timestamp
from typing import List, Optional


class SessionsClient:
    """Class definition for Sessions Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Sessions Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.session_service = SessionServiceStub(
            self.core_client.grpc_secure_channel
        )

    def get_session(self, session_id: str) -> SessionDetails:
        """
        Method to get session details by session ID

        :param session_id     : Session ID to get session details
        :type                 : ``` str ```

        :returns:
            Session Details
        """
        return self.core_client.grpc_exec(
            self.session_service.GetSession.with_call,
            SessionDetailsRequest(session_id=session_id),
        )

    def get_user_sessions(
        self, 
        user_id: str, 
        page_size: int = None, 
        page_token: str = None, 
        filter: UserSessionFilter = None
    ) -> UserSessionDetails:
        """
        Method to get all session details for a user with pagination and filtering support

        :param user_id        : User ID to get all session details for
        :type                 : ``` str ```
        :param page_size      : Number of sessions to return per page
        :type                 : ``` int ```
        :param page_token     : Token for pagination to get next/previous page
        :type                 : ``` str ```
        :param filter         : Filter to apply to sessions (status, time range)
        :type                 : ``` UserSessionFilter ```

        :returns:
            User Session Details with pagination info
        """
        request = UserSessionDetailsRequest(user_id=user_id)
        
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        if filter is not None:
            request.filter.CopyFrom(filter)
            
        return self.core_client.grpc_exec(
            self.session_service.GetUserSessions.with_call,
            request,
        )

    def revoke_session(self, session_id: str) -> RevokeSessionResponse:
        """
        Method to revoke a session for a user

        :param session_id     : Session ID to revoke
        :type                 : ``` str ```

        :returns:
            Revoke Session Response
        """
        return self.core_client.grpc_exec(
            self.session_service.RevokeSession.with_call,
            RevokeSessionRequest(session_id=session_id),
        )

    def revoke_all_user_sessions(self, user_id: str) -> RevokeAllUserSessionsResponse:
        """
        Method to revoke all sessions for a user

        :param user_id        : User ID to revoke all sessions for
        :type                 : ``` str ```

        :returns:
            Revoke All User Sessions Response
        """
        return self.core_client.grpc_exec(
            self.session_service.RevokeAllUserSessions.with_call,
            RevokeAllUserSessionsRequest(user_id=user_id),
        )

    @staticmethod
    def create_session_filter(
        status: Optional[List[str]] = None,
        start_time: Optional[Timestamp] = None,
        end_time: Optional[Timestamp] = None
    ) -> UserSessionFilter:
        """
        Helper method to create a UserSessionFilter for filtering sessions

        :param status         : List of session statuses to filter by
        :type                 : ``` List[str] ```
        :param start_time     : Filter sessions from this timestamp
        :type                 : ``` Timestamp ```
        :param end_time       : Filter sessions until this timestamp
        :type                 : ``` Timestamp ```

        :returns:
            UserSessionFilter object
        """
        filter_obj = UserSessionFilter()
        
        if status is not None:
            filter_obj.status.extend(status)
        if start_time is not None:
            filter_obj.start_time.CopyFrom(start_time)
        if end_time is not None:
            filter_obj.end_time.CopyFrom(end_time)
            
        return filter_obj
