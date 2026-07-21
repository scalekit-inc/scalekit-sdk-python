from basetest import BaseTest

from scalekit.v1.events.events_pb2 import Source


class TestEvents(BaseTest):
    """Class definition for Test Events Class"""

    def test_list_events_basic(self):
        """List events with no filter returns a response with events and total_size."""
        response = self.scalekit_client.events.list_events()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], "events"))
        self.assertTrue(hasattr(response[0], "total_size"))

    def test_list_events_with_filters(self):
        """List events accepts organization_id, source, and pagination filters."""
        response = self.scalekit_client.events.list_events(
            organization_id="org_does_not_exist",
            source="SCALEKIT",
            page_size=5,
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        # A nonexistent organization_id filters out all events, but the call still succeeds.
        self.assertEqual(len(response[0].events), 0)

    def test_list_events_with_auth_request_id_filter(self):
        """Filtering by a well-formed but non-matching auth_request_id returns zero events, not an error."""
        response = self.scalekit_client.events.list_events(
            auth_request_id="areq_does_not_exist"
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(len(response[0].events), 0)

    def test_list_events_invalid_source_raises_before_network_call(self):
        """An unrecognized source string is rejected client-side before any gRPC call is made."""
        with self.assertRaises(ValueError):
            self.scalekit_client.events.list_events(source="NOT_A_REAL_SOURCE")

    def test_list_events_accepts_enum_source(self):
        """source also accepts the raw enum value, not just its string name."""
        response = self.scalekit_client.events.list_events(source=Source.SCALEKIT)
        self.assertEqual(response[1].code().name, "OK")
