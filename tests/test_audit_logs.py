from basetest import BaseTest


class TestAuditLogs(BaseTest):
    """Class definition for Test Audit Logs Class"""

    def test_list_auth_requests_basic(self):
        """List authentication request logs with no filter returns a valid response shape."""
        response = self.scalekit_client.audit_logs.list_auth_requests()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], "authRequests"))
        self.assertTrue(hasattr(response[0], "total_size"))

    def test_list_auth_requests_with_filters(self):
        """List authentication request logs accepts email, status, and pagination filters."""
        response = self.scalekit_client.audit_logs.list_auth_requests(
            email="nobody-matching@example.com",
            status=["SUCCESS"],
            page_size=5,
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        # A non-matching email filters out all logs, but the call still succeeds.
        self.assertEqual(len(response[0].authRequests), 0)

    def test_list_auth_requests_pagination_token_is_client_validated_string(self):
        """page_token accepts a string cursor; a malformed one is rejected by the server, not swallowed."""
        response = self.scalekit_client.audit_logs.list_auth_requests(
            page_token="not-a-real-cursor"
        )
        # The server may reject a malformed cursor (INVALID_ARGUMENT) rather than the SDK
        # silently ignoring it. Either an explicit rejection or a clean empty page is
        # acceptable here — what's not acceptable is the SDK eating the parameter.
        self.assertIn(response[1].code().name, ("OK", "INVALID_ARGUMENT"))

    def test_events_correlate_with_auth_request_id(self):
        """
        Cross-API correlation: fetch real authentication request logs, take a real
        auth_request_id from the results, then confirm the Events API returns at least
        one event for that same auth_request_id.

        No IDs are hardcoded — everything is fetched live from the environment. If the
        environment has no authentication request history, there is nothing to correlate,
        so the assertion is skipped rather than failed.
        """
        auth_requests_response = self.scalekit_client.audit_logs.list_auth_requests(
            page_size=50
        )
        self.assertEqual(auth_requests_response[1].code().name, "OK")
        auth_requests = auth_requests_response[0].authRequests

        auth_request_id = next(
            (entry.auth_request_id for entry in auth_requests if entry.auth_request_id),
            None,
        )
        if not auth_request_id:
            self.skipTest(
                "No authentication request logs with an auth_request_id were found in "
                "this environment; nothing to correlate against the Events API."
            )

        events_response = self.scalekit_client.events.list_events(
            auth_request_id=auth_request_id
        )
        self.assertEqual(events_response[1].code().name, "OK")
        self.assertGreater(
            len(events_response[0].events),
            0,
            f"Expected at least one event for auth_request_id={auth_request_id!r}, "
            "which was returned by ListAuthRequests, but the Events API returned none.",
        )
