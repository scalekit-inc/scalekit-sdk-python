from pydantic import BaseModel


class DeleteCustomProviderResponse(BaseModel):
    """Response returned by ActionProviders.delete_custom_provider().

    This response is intentionally empty. A successful delete is indicated by
    this object being returned without an exception. Any server-side error
    (not found, permission denied, etc.) raises a ScalekitServerException subclass
    before this response is constructed.
    """

    @classmethod
    def from_proto(cls, proto_response) -> "DeleteCustomProviderResponse":
        """Decode a proto DeleteProviderResponse into a typed response.

        :param proto_response: Proto DeleteProviderResponse from providers_pb2.
        :returns: Empty DeleteCustomProviderResponse instance.
        :rtype: DeleteCustomProviderResponse
        """
        return cls()

    def to_dict(self) -> dict:
        """Serialize to a plain Python dict.

        :returns: Empty dict.
        :rtype: dict
        """
        return {}

    class Config:
        validate_assignment = True
