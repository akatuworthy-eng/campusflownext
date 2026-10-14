"""Regression tests for Engineer B review findings."""

import os
import stat
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from campusflow.storage import (
    validate_tickets,
    load_tickets,
    save_tickets,
)
from campusflow.tickets import create_ticket


class ReviewFixTests(unittest.TestCase):

    def test_unassigned_in_progress_ticket_rejected(self):
        tickets = []
        create_ticket(
            tickets, "Printer issue", "Hardware", "low", 1
        )
        tickets[0]["status"] = "in_progress"

        with self.assertRaisesRegex(
            ValueError, "without an assignee"
        ):
            validate_tickets(tickets)

    def test_invalid_workflow_file_preserved(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            tickets = []
            create_ticket(
                tickets, "Wi-Fi issue", "Network", "high", 12
            )
            save_tickets(tickets, path)

            original = path.read_text()
            tickets[0]["status"] = "in_progress"

            with self.assertRaises(ValueError):
                save_tickets(tickets, path)

            self.assertEqual(path.read_text(), original)
            self.assertEqual(
                load_tickets(path)[0]["status"], "open"
            )

    def test_unassigned_resolved_ticket_rejected(self):
        tickets = []
        create_ticket(
            tickets, "Printer issue", "Hardware", "low", 1
        )
        tickets[0]["status"] = "resolved"

        with self.assertRaisesRegex(
            ValueError, "resolved without an assignee"
        ):
            validate_tickets(tickets)

    def test_assigned_resolved_ticket_is_valid(self):
        tickets = []
        create_ticket(
            tickets, "Printer issue", "Hardware", "low", 1
        )
        tickets[0]["assigned_to"] = "Support A"
        tickets[0]["status"] = "resolved"

        validate_tickets(tickets)

    @unittest.skipUnless(
        os.name == "posix", "POSIX file permissions required"
    )
    def test_atomic_save_preserves_existing_permissions(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("[]")
            path.chmod(0o640)

            before = stat.S_IMODE(path.stat().st_mode)

            save_tickets([], path)

            after = stat.S_IMODE(path.stat().st_mode)
            self.assertEqual(before, after)
            self.assertEqual(after, 0o640)


if __name__ == "__main__":
    unittest.main()
