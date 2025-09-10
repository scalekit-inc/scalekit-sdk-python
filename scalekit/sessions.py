from scalekit.core import CoreClient
from scalekit.v1.sessions.sessions_pb2 import *
from scalekit.v1.sessions.sessions_pb2_grpc import SessionServiceStub


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

    def get_user_sessions(self, user_id: str) -> UserSessionDetails:
        """
        Method to get all session details for a user

        :param user_id        : User ID to get all session details for
        :type                 : ``` str ```

        :returns:
            User Session Details
        """
        return self.core_client.grpc_exec(
            self.session_service.GetUserSessions.with_call,
            UserSessionDetailsRequest(user_id=user_id),
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
