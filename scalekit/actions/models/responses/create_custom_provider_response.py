from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.custom_provider import Provider


class CreateCustomProviderResponse(BaseModel):
    """Response returned by ActionProviders.create_custom_provider().

    Contains the fully-decoded provider as created by the server, including
    the server-assigned identifier and all decoded auth_patterns.
    """

    provider: Optional[Provider] = Field(
        None,
        description=(
            "The newly created provider. Contains the server-assigned identifier, "
            "all provided fields, and fully decoded auth_patterns. "
            "None only if the server returned an empty response body."
        ),
    )

    @classmethod
    def from_proto(cls, proto_response) -> "CreateCustomProviderResponse":
        """Decode a proto CreateProviderResponse into a typed response.

        :param proto_response: Proto CreateProviderResponse from providers_pb2.
        :returns: CreateCustomProviderResponse with provider decoded.
        :rtype: CreateCustomProviderResponse
        """
        provider = None
        if proto_response.provider:
            provider = Provider.from_proto(proto_response.provider)
        return cls(provider=provider)

    def to_dict(self) -> dict:
        """Serialize to a plain Python dict.

        :returns: Dict with a 'provider' key. Value is None if provider is absent.
        :rtype: dict
        """
        return {"provider": self.provider.model_dump() if self.provider else None}

    class Config:
        validate_assignment = True
