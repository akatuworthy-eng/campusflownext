"""Engineer A: failed saves and corrupted notes must not alter valid data."""
import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campusflow.notes import add_note
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class AtomicStorageTestCase(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Router offline", "Network", "high", 12)

    def test_failed_replace_preserves_previous_json(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            save_tickets(self.tickets, path)
            original_bytes = path.read_bytes()
            self.tickets[0]["title"] = "Router updated"
            with patch("campusflow.storage.os.replace", side_effect=OSError("disk error")):
                with self.assertRaises(ValueError):
                    save_tickets(self.tickets, path)
            self.assertEqual(path.read_bytes(), original_bytes)
            self.assertEqual(list(Path(folder).glob("*.tmp")), [])

    def test_unserializable_field_does_not_truncate_existing_file(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            save_tickets(self.tickets, path)
            original_bytes = path.read_bytes()
            self.tickets[0]["unserializable_extra"] = object()
            with self.assertRaises(ValueError):
                save_tickets(self.tickets, path)
            self.assertEqual(path.read_bytes(), original_bytes)

    def test_invalid_loaded_note_rejected_without_modifying_file(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            invalid = copy.deepcopy(self.tickets)
            invalid[0]["notes"] = [{
                "note_id": "N001", "author": "Staff A", "message": "no"
            }]
            path.write_text(json.dumps(invalid), encoding="utf-8")
            original_bytes = path.read_bytes()
            with self.assertRaises(ValueError):
                load_tickets(path)
            self.assertEqual(path.read_bytes(), original_bytes)
            self.assertEqual(self.tickets[0]["notes"], [])

    def test_invalid_existing_note_blocks_add_without_mutation(self):
        first = add_note(self.tickets, "T001", "Staff A", "Router inspected")
        self.tickets[0]["notes"][0]["message"] = "no"
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Staff B", "Checking the cable")
        self.assertEqual(self.tickets, before)
        self.assertEqual(first["note_id"], "N001")


if __name__ == "__main__":
    unittest.main()
