"""CLI search regression tests."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import run_cli
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_status


class TestSearchCLI(unittest.TestCase):

    def make_tickets(self, path):
        tickets = []
        create_ticket(
            tickets, "Wi-Fi outage", "Network", "high", 12
        )
        create_ticket(
            tickets, "Broken laptop", "Hardware", "low", 1
        )
        create_ticket(
            tickets, "Wi-Fi login", "Network", "medium", 3
        )
        assign_ticket(tickets, "T003", "Support A")
        update_status(tickets, "T003", "in_progress")
        save_tickets(tickets, path)

    def run_search(self, path, answers):
        output = StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                result = run_cli(path)
        self.assertEqual(result, 0)
        return output.getvalue()

    def test_combined_filters(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_tickets(path)

            output = self.run_search(
                path,
                ["10", "WI-FI", "Network", "open",
                 "critical", "n", "9"],
            )

            self.assertIn("Found 1 ticket(s)", output)
            self.assertIn("T001 | Wi-Fi outage", output)
            self.assertNotIn("T003 | Wi-Fi login", output)

    def test_invalid_category_reprompts(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_tickets(path)

            output = self.run_search(
                path,
                ["10", "", "Transport", "Network",
                 "", "", "", "9"],
            )

            self.assertIn("Invalid category", output)
            self.assertIn("Found 2 ticket(s)", output)

    def test_invalid_status_and_priority_reprompt(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_tickets(path)

            output = self.run_search(
                path,
                ["10", "Wi-Fi", "Network", "waiting",
                 "open", "urgent", "critical", "n", "9"],
            )

            self.assertIn("Invalid status", output)
            self.assertIn("Invalid priority", output)
            self.assertIn("Found 1 ticket(s)", output)

    def test_no_matches_does_not_modify_tickets(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_tickets(path)

            before = load_tickets(path)

            output = self.run_search(
                path,
                ["10", "nonexistent", "", "",
                 "", "", "9"],
            )

            self.assertIn("No matching tickets", output)
            self.assertEqual(load_tickets(path), before)


if __name__ == "__main__":
    unittest.main()
