from basetest import BaseTest


class TestEvents(BaseTest):
    """ Class definition for Test Events Class """

    def test_list_events_paginated(self):
        """ Method to test list events paginated """
        response = self.scalekit_client.events.list_events_paginated(
            page_size=10, page_token=""
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

        # events is iterable (may be empty)
        events = list(response[0].events)
        self.assertIsNotNone(events)

        # reading pagination tokens must not throw
        _ = response[0].next_page_token
        _ = response[0].prev_page_token
