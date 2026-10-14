
"""Structured follow-up notes for CampusFlow."""

import re

from campusflow.workflow import _find_ticket


def add_note(tickets, ticket_id, author, message):
    """Add a validated note to an open or in-progress ticket."""

    ticket = _find_ticket(tickets, ticket_id)

    if ticket.get("status") not in ("open", "in_progress"):
        raise ValueError("Resolved tickets cannot accept notes")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Author cannot be blank")

    if not isinstance(message, str):
        raise ValueError("Message must be text")

    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError("Message must contain 5-300 characters")

    notes = ticket.get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Notes must be a list")

    seen_ids = set()
    highest_number = 0

    for existing in notes:
        if not isinstance(existing, dict):
            raise ValueError("Invalid existing note")

        note_id = existing.get("note_id")

        if (
            not isinstance(note_id, str)
            or not re.fullmatch(r"N[0-9]{3,}", note_id)
        ):
            raise ValueError("Invalid note ID")

        number = int(note_id[1:])

        if number < 1 or note_id != f"N{number:03d}":
            raise ValueError("Invalid note ID")

        if note_id in seen_ids:
            raise ValueError("Duplicate note ID")

        seen_ids.add(note_id)
        highest_number = max(highest_number, number)

    new_note = {
        "note_id": f"N{highest_number + 1:03d}",
        "author": author.strip(),
        "message": message,
    }

    if "notes" not in ticket:
        ticket["notes"] = []

    ticket["notes"].append(new_note)

    return new_note
