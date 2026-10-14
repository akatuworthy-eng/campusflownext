
import copy
import unittest

from campusflow.tickets import create_ticket
from campusflow.notes import add_note
from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
)


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = []
        create_ticket(
            self.tickets, "Wi-Fi outage",
            "Network", "high", 12
        )

    def test_new_ticket_has_empty_notes(self):
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_note_ids_increment(self):
        first = add_note(
            self.tickets, "T001",
            "Mentor A", "Router inspected"
        )
        second = add_note(
            self.tickets, "T001",
            "Mentor B", "Checking cables"
        )

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_invalid_note_preserves_data(self):
        before = copy.deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(
                self.tickets, "T001",
                "Mentor A", "Hi"
            )

        self.assertEqual(self.tickets, before)

    def test_resolved_ticket_requires_reopen(self):
        assign_ticket(self.tickets, "T001", "Support A")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            add_note(
                self.tickets, "T001",
                "Mentor A", "Checking hardware"
            )

        reopen_ticket(self.tickets, "T001")

        note = add_note(
            self.tickets, "T001",
            "Mentor A", "Issue reopened"
        )

        self.assertEqual(note["note_id"], "N001")


if __name__ == "__main__":
    unittest.main()
