from typing import List

from pydantic import BaseModel, Field

from scalekit.actions.models.custom_provider import Provider


class ListProvidersResponse(BaseModel):
    """Response returned by ActionProviders.list_providers().

    Contains a page of providers matching the request filters and pagination
    cursor for fetching the next page.
    """

    providers: List[Provider] = Field(
        default_factory=list,
        description=(
            "List of providers in the current page. Each Provider has fully decoded "
            "auth_patterns. Empty list if no providers match the filter."
        ),
    )
    next_page_token: str = Field(
        "",
        description=(
            "Pagination cursor for the next page. Pass this value as "
            "ListProvidersRequest.page_token in a subsequent call to fetch the next "
            "page. Empty string when this is the last page."
        ),
    )
    total_size: int = Field(
        0,
        description=(
            "Total number of providers matching the filter across all pages. "
            "May be 0 if the server does not support total count."
        ),
    )

    @classmethod
    def from_proto(cls, proto_response) -> "ListProvidersResponse":
        """Decode a proto ListProvidersResponse into a typed response.

        :param proto_response: Proto ListProvidersResponse from providers_pb2.
        :returns: ListProvidersResponse with providers decoded.
        :rtype: ListProvidersResponse
        """
        return cls(
            providers=[Provider.from_proto(p) for p in proto_response.providers],
            next_page_token=proto_response.next_page_token,
            total_size=proto_response.total_size,
        )

    def to_dict(self) -> dict:
        """Serialize to a plain Python dict.

        :returns: Dict with 'providers', 'next_page_token', and 'total_size' keys.
        :rtype: dict
        """
        return {
            "providers": [p.model_dump() for p in self.providers],
            "next_page_token": self.next_page_token,
            "total_size": self.total_size,
        }

    class Config:
        validate_assignment = True
