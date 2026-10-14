"""Tests for enhanced CampusFlow reports."""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from campusflow.reports import generate_report
from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
)
from main import display_report


class TestEnhancedReports(unittest.TestCase):

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
            self.tickets, "Software issue",
            "Software", "medium", 3
        )

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertTrue(
            all(v == 0 for v in report["by_category"].values())
        )

    def test_category_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["total"], 3)
        self.assertEqual(
            report["by_category"],
            {
                "Network": 1,
                "Hardware": 1,
                "Software": 1,
                "Other": 0,
            }
        )

    def test_resolution_counts_and_reopening(self):
        assign_ticket(self.tickets, "T001", "Support A")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        assign_ticket(self.tickets, "T003", "Support B")
        update_status(self.tickets, "T003", "in_progress")

        report = generate_report(self.tickets)

        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["unresolved"], 2)
        self.assertAlmostEqual(
            report["resolution_percentage"], 100 / 3
        )
        self.assertEqual(
            sum(report["by_status"].values()), 3
        )

        reopen_ticket(self.tickets, "T001")
        updated = generate_report(self.tickets)

        self.assertEqual(updated["resolved"], 0)
        self.assertEqual(updated["unresolved"], 3)
        self.assertEqual(updated["resolution_percentage"], 0.0)

    def test_cli_displays_enhanced_report(self):
        report = generate_report(self.tickets)
        output = StringIO()

        with redirect_stdout(output):
            display_report(report)

        text = output.getvalue()
        self.assertIn("By category:", text)
        self.assertIn("Unresolved tickets: 3", text)
        self.assertIn("Resolved tickets: 0", text)
        self.assertIn("Resolution percentage: 0.00%", text)


if __name__ == "__main__":
    unittest.main()
