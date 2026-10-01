"""Response model for ``ActionClient.search_connected_accounts``."""

from typing import cast

from scalekit.actions.models.responses.list_connected_accounts_response import (
    ListConnectedAccountsResponse,
)
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    SearchConnectedAccountsResponse as SearchConnectedAccountsResponseProto,
)


class SearchConnectedAccountsResponse(ListConnectedAccountsResponse):
    """One page of connected accounts that match a search query.

    Has the same fields, aliases and ``to_dict()`` output as
    ``ListConnectedAccountsResponse``, so code that reads a list page can read a
    search page unchanged.

    Attributes:
        connected_accounts: The matching connected accounts on this page, without
            authorization details. Empty when nothing matches.
        total_count: Total number of matches across all pages (``total_size`` on
            the wire). ``None`` when the server reports zero.
        next_page_token: Pass as ``page_token`` to fetch the next page. ``None``
            on the last page.
        previous_page_token: Token for the previous page (``prev_page_token`` on
            the wire). ``None`` on the first page.

    Example:
        result = client.actions.search_connected_accounts(query="gmail")
        print(result.total_count)
        for account in result.connected_accounts:
            print(account.identifier, account.connector, account.status)
    """

    @classmethod
    def from_proto(
        cls, proto_response: SearchConnectedAccountsResponseProto
    ) -> "SearchConnectedAccountsResponse":
        """Build the model from the ``SearchConnectedAccountsResponse`` proto message.

        The search and list proto responses have identical fields, so the
        mapping is inherited from ``ListConnectedAccountsResponse.from_proto``,
        which constructs ``cls`` and therefore returns this subclass.

        Args:
            proto_response: The proto message returned by
                ``ConnectedAccountsClient.search_connected_accounts``.

        Returns:
            The mapped response. Empty strings become ``None``.

        Example:
            response, _ = client.connected_accounts.search_connected_accounts(query="gmail")
            page = SearchConnectedAccountsResponse.from_proto(response)
        """
        return cast(
            "SearchConnectedAccountsResponse",
            super().from_proto(proto_response),
        )
