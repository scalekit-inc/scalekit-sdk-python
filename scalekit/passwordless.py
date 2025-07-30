from typing import Optional, Dict, Union

from scalekit.core import CoreClient
from scalekit.v1.auth.passwordless_pb2 import *
from scalekit.v1.auth.passwordless_pb2_grpc import PasswordlessServiceStub



# String to enum mapping for template types
_TEMPLATE_TYPE_MAP = {
    "UNSPECIFIED": TemplateType.UNSPECIFIED,
    "SIGNIN": TemplateType.SIGNIN,
    "SIGNUP": TemplateType.SIGNUP,
}

def _convert_template_type(template: Union[str, TemplateType, None]) -> Optional[TemplateType]:
    """Convert string or enum to TemplateType enum"""
    if template is None:
        return None
    if isinstance(template, str):
        template_upper = template.upper()
        if template_upper in _TEMPLATE_TYPE_MAP:
            return _TEMPLATE_TYPE_MAP[template_upper]
        else:
            raise ValueError(f"Invalid template type: {template}. Valid options are: {list(_TEMPLATE_TYPE_MAP.keys())}")
    return template


class PasswordlessClient:
    """Class definition for Passwordless Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Passwordless Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.passwordless_service = PasswordlessServiceStub(
            self.core_client.grpc_secure_channel
        )

    def send_passwordless_email(
        self,
        email: str,
        template: Optional[Union[str, TemplateType]] = None,
        magiclink_auth_uri: Optional[str] = None,
        state: Optional[str] = None,
        expires_in: Optional[int] = None,
        template_variables: Optional[Dict[str, str]] = None
    ) -> SendPasswordlessResponse:
        """
        Method to send passwordless authentication email

        :param email              : Email address to send the passwordless authentication to
        :type                     : ``` str ```
        :param template           : Template type ("SIGNIN", "SIGNUP", or "UNSPECIFIED")
        :type                     : ``` str or TemplateType ```
        :param magiclink_auth_uri : Callback URL for magic link authentication
        :type                     : ``` str ```
        :param state              : Custom state parameter to maintain application state
        :type                     : ``` str ```
        :param expires_in         : Expiration time in seconds (default: 300)
        :type                     : ``` int ```
        :param template_variables : Key-value pairs for email template personalization
        :type                     : ``` dict ```

        :returns:
            Send Passwordless Response
        """
        request = SendPasswordlessRequest(email=email)
        
        # Convert template string to enum if needed
        template_enum = _convert_template_type(template)
        if template_enum is not None:
            request.template = template_enum
            
        if magiclink_auth_uri is not None:
            request.magiclink_auth_uri = magiclink_auth_uri
        if state is not None:
            request.state = state
        if expires_in is not None:
            request.expires_in = expires_in
        if template_variables is not None:
            request.template_variables.update(template_variables)
        
        return self.core_client.grpc_exec(
            self.passwordless_service.SendPasswordlessEmail.with_call,
            request,
        )

    def verify_passwordless_email(
        self,
        code: Optional[str] = None,
        link_token: Optional[str] = None,
        auth_request_id: Optional[str] = None
    ) -> VerifyPasswordLessResponse:
        """
        Method to verify passwordless authentication

        :param code            : The OTP code received via email
        :type                  : ``` str ```
        :param link_token      : The token from the magic link URL
        :type                  : ``` str ```
        :param auth_request_id : The authentication request ID from send request
        :type                  : ``` str ```

        :returns:
            Verify Passwordless Response
        """
        request = VerifyPasswordLessRequest()
        
        if code is not None:
            request.code = code
        elif link_token is not None:
            request.link_token = link_token
            
        if auth_request_id is not None:
            request.auth_request_id = auth_request_id
        
        return self.core_client.grpc_exec(
            self.passwordless_service.VerifyPasswordlessEmail.with_call,
            request,
        )

    def resend_passwordless_email(
        self,
        auth_request_id: str
    ) -> SendPasswordlessResponse:
        """
        Method to resend passwordless authentication email

        :param auth_request_id : The authentication request ID from original send request
        :type                  : ``` str ```

        :returns:
            Send Passwordless Response
        """
        return self.core_client.grpc_exec(
            self.passwordless_service.ResendPasswordlessEmail.with_call,
            ResendPasswordlessRequest(auth_request_id=auth_request_id),
        ) 