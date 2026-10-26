"""The client.actions response models must carry every field the backend sends.

Credential-free: builds real protobuf messages and converts them with from_proto().
"""
import json

from google.protobuf.struct_pb2 import ListValue

from scalekit.actions.models.custom_provider import Provider
from scalekit.actions.models.responses.get_connected_account_auth_response import (
    ConnectedAccount,
)
from scalekit.actions.models.responses.list_connected_accounts_response import (
    ConnectedAccountForList,
    ListConnectedAccountsResponse,
)
from scalekit.actions.models.responses.list_providers_response import (
    ListProvidersResponse,
)
from scalekit.v1.connected_accounts import connected_accounts_pb2 as ca_pb2
from scalekit.v1.providers import providers_pb2


def test_listed_connected_account_carries_id_connection_id_and_org_wide_flag():
    proto = ca_pb2.ListConnectedAccountsResponse(
        connected_accounts=[
            ca_pb2.ConnectedAccountForList(
                id="ca_123",
                connection_id="conn_456",
                is_org_wide_credential=True,
                identifier="user@example.com",
                provider="SLACK",
                connector="slack-abc",
            )
        ],
        total_size=1,
    )

    account = ListConnectedAccountsResponse.from_proto(proto).connected_accounts[0]

    assert account.id == "ca_123"
    assert account.connection_id == "conn_456"
    assert account.is_org_wide_credential is True
    assert account.to_dict()["id"] == "ca_123"
    assert account.to_dict()["connection_id"] == "conn_456"
    assert account.to_dict()["is_org_wide_credential"] is True


def test_listed_connected_account_without_the_new_fields_keeps_defaults():
    account = ConnectedAccountForList.from_proto(
        ca_pb2.ConnectedAccountForList(identifier="user@example.com")
    )

    assert account.id is None
    assert account.connection_id is None
    assert account.is_org_wide_credential is False
    assert account.identifier == "user@example.com"


def test_connected_account_from_get_carries_connection_id_and_org_wide_flag():
    account = ConnectedAccount.from_proto(
        ca_pb2.ConnectedAccount(
            id="ca_123",
            connection_id="conn_456",
            is_org_wide_credential=True,
            identifier="user@example.com",
        )
    )

    assert account.id == "ca_123"
    assert account.connection_id == "conn_456"
    assert account.is_org_wide_credential is True


def test_provider_carries_id_categories_display_priority_and_coming_soon():
    proto = providers_pb2.Provider(
        id="prvd_789",
        identifier="MIREYE",
        display_name="Mireye",
        categories=["AI", "Analytics", "Search"],
        display_priority=50,
        coming_soon=True,
        auth_patterns=ListValue(),
    )

    provider = Provider.from_proto(proto)

    assert provider.id == "prvd_789"
    assert provider.categories == ["AI", "Analytics", "Search"]
    assert provider.display_priority == 50
    assert provider.coming_soon is True
    assert provider.identifier == "MIREYE"


def test_provider_constructed_without_the_new_fields_still_works():
    provider = Provider(identifier="X", display_name="X")

    assert provider.id == ""
    assert provider.categories == []
    assert provider.display_priority == 0
    assert provider.coming_soon is False


def test_list_providers_response_carries_the_previous_page_token():
    proto = providers_pb2.ListProvidersResponse(
        providers=[providers_pb2.Provider(identifier="A", auth_patterns=ListValue())],
        next_page_token="next",
        prev_page_token="prev",
        total_size=7,
    )

    response = ListProvidersResponse.from_proto(proto)

    assert response.prev_page_token == "prev"
    assert response.next_page_token == "next"
    assert response.total_size == 7
    assert response.to_dict()["prev_page_token"] == "prev"
    json.dumps(response.to_dict(), default=str)
