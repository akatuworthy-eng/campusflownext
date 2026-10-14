"""Combined Engineer A/B notes CLI regression tests."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    update_status,
)
from main import run_cli


class TestNotesCLI(unittest.TestCase):

    def make_ticket(self, path, resolved=False):
        tickets = []
        create_ticket(
            tickets, "Router issue", "Network", "high", 12
        )
        if resolved:
            assign_ticket(tickets, "T001", "Support A")
            update_status(tickets, "T001", "in_progress")
            update_status(tickets, "T001", "resolved")
        save_tickets(tickets, path)

    def run_commands(self, path, commands):
        output = StringIO()

        with patch("builtins.input", side_effect=commands):
            with redirect_stdout(output):
                result = run_cli(path)

        self.assertEqual(result, 0)
        return output.getvalue()

    def test_add_and_view_note_after_reload(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_ticket(path)

            output = self.run_commands(
                path,
                [
                    "12", "t001", "Mentor A",
                    "Router inspected",
                    "13", "T001", "9",
                ],
            )

            self.assertIn("Added note N001", output)
            self.assertIn(
                "N001 | Mentor A: Router inspected", output
            )
            saved = load_tickets(path)
            self.assertEqual(len(saved[0]["notes"]), 1)

    def test_invalid_note_does_not_consume_id(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_ticket(path)

            output = self.run_commands(
                path,
                [
                    "12", "T001", "Staff A", "Hi",
                    "12", "T001", "Staff A",
                    "Checking the router",
                    "9",
                ],
            )

            self.assertIn("Message must contain", output)
            self.assertIn("Added note N001", output)
            self.assertEqual(
                len(load_tickets(path)[0]["notes"]), 1
            )

    def test_resolved_note_requires_reopen(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_ticket(path, resolved=True)

            output = self.run_commands(
                path,
                [
                    "12", "T001", "Staff A",
                    "Investigating again",
                    "5", "T001", "reopen",
                    "12", "T001", "Staff A",
                    "Investigating again",
                    "9",
                ],
            )

            self.assertIn(
                "Resolved tickets cannot accept notes", output
            )
            self.assertIn("Added note N001", output)
            self.assertEqual(
                load_tickets(path)[0]["status"], "open"
            )

    def test_view_empty_notes(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            self.make_ticket(path)

            output = self.run_commands(
                path, ["13", "T001", "9"]
            )

            self.assertIn("No notes for T001", output)


if __name__ == "__main__":
    unittest.main()
