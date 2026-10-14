"""Unit tests for combined ticket search."""

import copy
import unittest

from campusflow.search import search_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status


class TestTicketSearch(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        create_ticket(
            self.tickets, "Wi-Fi outage",
            "Network", "high", 12
        )
        create_ticket(
            self.tickets, "Broken laptop",
            "Hardware", "low", 1
        )
        create_ticket(
            self.tickets, "Wi-Fi login problem",
            "Network", "medium", 3
        )
        create_ticket(
            self.tickets, "Software install",
            "Software", "high", 2
        )

        assign_ticket(self.tickets, "T003", "Support A")
        update_status(self.tickets, "T003", "in_progress")

    def ids(self, results):
        return [ticket["id"] for ticket in results]

    def test_case_insensitive_title_search(self):
        results = search_tickets(self.tickets, title="WI-FI")
        self.assertEqual(self.ids(results), ["T001", "T003"])

    def test_combined_filters_use_and(self):
        results = search_tickets(
            self.tickets,
            title="wi-fi",
            category="Network",
            status="open",
            priority="critical",
        )
        self.assertEqual(self.ids(results), ["T001"])

    def test_search_by_status_and_priority(self):
        results = search_tickets(
            self.tickets,
            status="in_progress",
            priority="medium",
        )
        self.assertEqual(self.ids(results), ["T003"])

    def test_empty_filters_return_all_tickets(self):
        results = search_tickets(self.tickets)
        self.assertEqual(len(results), 4)

    def test_invalid_filters_are_rejected(self):
        for name, value in (
            ("category", "Transport"),
            ("status", "waiting"),
            ("priority", "urgent"),
        ):
            with self.subTest(filter=name):
                with self.assertRaises(ValueError):
                    search_tickets(self.tickets, **{name: value})

    def test_search_does_not_mutate_tickets(self):
        original = copy.deepcopy(self.tickets)
        search_tickets(
            self.tickets, title="Wi-Fi", category="Network"
        )
        self.assertEqual(self.tickets, original)

    def test_optional_priority_sorting(self):
        results = search_tickets(
            self.tickets, sort_by_priority=True
        )
        self.assertEqual(
            self.ids(results),
            ["T001", "T004", "T003", "T002"],
        )


if __name__ == "__main__":
    unittest.main()
