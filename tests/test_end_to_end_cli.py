"""End-to-end CLI smoke tests using an actual Python child process.

All ticket data is written under TemporaryDirectory, never to the
repository's data/tickets.json.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


MAIN = Path(__file__).resolve().parents[1] / "main.py"


def run_cli_script(folder, answers):
    """Run the real CLI, sending one newline-delimited input per prompt."""
    completed = subprocess.run(
        [sys.executable, str(MAIN)],
        cwd=folder,
        input="\n".join(answers) + "\n",
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"CampusFlow exited {completed.returncode}:\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )
    return completed.stdout


def get_saved_tickets(folder):
    path = Path(folder) / "data" / "tickets.json"
    return json.loads(path.read_text(encoding="utf-8"))


class CampusFlowInteractiveSmokeTests(unittest.TestCase):
    def test_all_thirteen_menu_options_and_reload(self):
        with TemporaryDirectory() as folder:
            output = run_cli_script(
                folder,
                [
                    "1", "Campus Wi-Fi outage", "Network", "high", "12",
                    "1", "Broken laptop", "Hardware", "low", "1",
                    "2",
                    "3", "t001",
                    "4", "T001", "Support A",
                    "5", "T001", "in_progress",
                    "12", "T001", "Support A", "Router check in progress",
                    "13", "t001",
                    "10", "WI-FI", "network", "in_progress",
                    "critical", "y",
                    "7",
                    "6",
                    "11", "invalid", "B", "C", "B", "D", "A", "C",
                    "8",
                    "9",
                ],
            )

            for expected in (
                "Created T001.",
                "Created T002.",
                "Ticket assigned.",
                "Status updated.",
                "Added note N001.",
                "N001 | Support A: Router check in progress",
                "Found 1 ticket(s):",
                "T001 | Campus Wi-Fi outage | Network | critical",
                "Total tickets: 2",
                "Resolution percentage: 0.00%",
                "Invalid answer. Choose A, B, C or D.",
                "Final score: 6/6",
                "Tickets saved. Goodbye.",
            ):
                with self.subTest(expected=expected):
                    self.assertIn(expected, output)

            tickets = get_saved_tickets(folder)
            self.assertEqual(len(tickets), 2)
            self.assertEqual(tickets[0]["priority"], "critical")
            self.assertEqual(tickets[0]["status"], "in_progress")
            self.assertEqual(tickets[0]["assigned_to"], "Support A")
            self.assertEqual(tickets[0]["notes"][0]["note_id"], "N001")
            self.assertEqual(tickets[1]["status"], "open")
            self.assertEqual(tickets[1]["priority"], "low")

            # A separate invocation proves that the saved data reloads.
            restart_output = run_cli_script(
                folder, ["13", "T001", "7", "9"]
            )
            self.assertIn(
                "N001 | Support A: Router check in progress",
                restart_output,
            )
            self.assertIn("Total tickets: 2", restart_output)

    def test_invalid_note_resolved_workflow_search_and_reopen(self):
        with TemporaryDirectory() as folder:
            output = run_cli_script(
                folder,
                [
                    "1", "Printer issue", "Hardware", "medium", "3",
                    "12", "T001", "Staff A", "Hi",
                    "4", "T001", "Support A",
                    "5", "T001", "in_progress",
                    "5", "T001", "resolved",
                    "12", "T001", "Staff A", "Working on it again",
                    "7",
                    "10", "nonexistent", "", "", "", "", "n",
                    "5", "T001", "reopen",
                    "12", "T001", "Staff A", "Investigating again",
                    "7",
                    "9",
                ],
            )

            self.assertIn("Message must contain 5-300 characters", output)
            self.assertIn("Resolved tickets cannot accept notes", output)
            self.assertIn("Resolution percentage: 100.00%", output)
            self.assertIn("No matching tickets.", output)
            self.assertIn("Resolution percentage: 0.00%", output)
            self.assertIn("Added note N001.", output)

            tickets = get_saved_tickets(folder)
            self.assertEqual(len(tickets), 1)
            self.assertEqual(tickets[0]["status"], "open")
            self.assertEqual(tickets[0]["assigned_to"], "Support A")
            self.assertEqual(len(tickets[0]["notes"]), 1)
            self.assertEqual(tickets[0]["notes"][0]["note_id"], "N001")


if __name__ == "__main__":
    unittest.main()
