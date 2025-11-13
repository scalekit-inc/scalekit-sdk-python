from typing import Optional, Dict, Any, Mapping
from google.protobuf.json_format import ParseDict
from google.protobuf.empty_pb2 import Empty

from scalekit.core import CoreClient
from scalekit.v1.auth import auth_pb2
from scalekit.v1.auth.auth_pb2_grpc import AuthServiceStub


class AuthClient:
    """Class definition for Auth Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Auth Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.auth_service = AuthServiceStub(
            self.core_client.grpc_secure_channel
        )

    def update_login_user_details(
        self,
        connection_id: str,
        login_request_id: str,
        user: Optional[Mapping[str, Any]] = None,
    ) -> Empty:
        """
        Method to update user details for a login request

        :param connection_id     : Connection ID. Unique ID for the connection
        :type                     : ``` str ```
        :param login_request_id   : Login Request ID that was shared as part of authorization initiate
        :type                     : ``` str ```
        :param user               : User details as dictionary with optional fields:
                                     * sub: Subject identifier for the user
                                     * email: User's primary email address
                                     * given_name: User's first name
                                     * family_name: User's last name
                                     * email_verified: Whether email is verified
                                     * phone_number: User's primary phone number
                                     * phone_number_verified: Whether phone is verified
                                     * name: Full display name of the user
                                     * preferred_username: User's preferred username
                                     * picture: URL to user's profile picture
                                     * gender: User's gender
                                     * locale: User's locale preference
                                     * groups: List of group names or IDs
                                     * custom_attributes: Custom attributes as dict
        :type                     : ``` dict ```

        :returns:
            Empty response
        """

        user_data: Dict[str, Any] = {}
        if user is not None:
            if isinstance(user, Mapping):
                user_data.update(user)  
            else:
                raise TypeError("user must be a mapping-compatible object")

        user_msg = ParseDict(user_data, auth_pb2.User())

        # Create request
        request = auth_pb2.UpdateLoginUserDetailsRequest(
            connection_id=connection_id,
            login_request_id=login_request_id,
            user=user_msg
        )

        return self.core_client.grpc_exec(
            self.auth_service.UpdateLoginUserDetails.with_call,
            request,
        )

