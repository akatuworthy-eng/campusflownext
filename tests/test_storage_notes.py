import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from campusflow.tickets import create_ticket
from campusflow.notes import add_note
from campusflow.storage import load_tickets, save_tickets


class TestStorageNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = []
        create_ticket(
            self.tickets, "Wi-Fi outage",
            "Network", "high", 12
        )

    def test_notes_survive_reload(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            add_note(
                self.tickets, "T001",
                "Mentor A", "Router inspected"
            )

            save_tickets(self.tickets, path)
            restored = load_tickets(path)

            self.assertEqual(
                restored[0]["notes"][0]["note_id"],
                "N001"
            )

            next_note = add_note(
                restored, "T001",
                "Mentor B", "Checking cables"
            )

            self.assertEqual(next_note["note_id"], "N002")

    def test_duplicate_note_ids_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            first = add_note(
                self.tickets, "T001",
                "Mentor A", "Router inspected"
            )

            add_note(
                self.tickets, "T001",
                "Mentor B", "Checking cables"
            )

            self.tickets[0]["notes"][1]["note_id"] = first["note_id"]

            with self.assertRaises(ValueError):
                save_tickets(self.tickets, path)

            self.assertFalse(path.exists())

    def test_invalid_note_message_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            self.tickets[0]["notes"] = [{
                "note_id": "N001",
                "author": "Mentor A",
                "message": "Hi"
            }]

            with self.assertRaises(ValueError):
                save_tickets(self.tickets, path)

    def test_old_tickets_load_without_notes(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            del self.tickets[0]["notes"]
            path.write_text(
                json.dumps(self.tickets),
                encoding="utf-8"
            )

            restored = load_tickets(path)

            self.assertEqual(restored[0]["notes"], [])


if __name__ == "__main__":
    unittest.main()
