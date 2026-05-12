from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.custom_provider import Provider


class UpdateCustomProviderResponse(BaseModel):
    """Response returned by ActionProviders.update_custom_provider().

    Contains the provider's state after the update has been applied. All fields
    reflect the current server-side values — not just the fields that were changed.
    """

    provider: Optional[Provider] = Field(
        None,
        description=(
            "The updated provider reflecting its full current state after the update. "
            "None only if the server returned an empty response body."
        ),
    )

    @classmethod
    def from_proto(cls, proto_response) -> "UpdateCustomProviderResponse":
        """Decode a proto UpdateProviderResponse into a typed response.

        :param proto_response: Proto UpdateProviderResponse from providers_pb2.
        :returns: UpdateCustomProviderResponse with provider decoded.
        :rtype: UpdateCustomProviderResponse
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
