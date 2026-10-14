"""CLI operations for structured follow-up notes."""

from campusflow.notes import add_note
from campusflow.workflow import _find_ticket


def prompt_add_note(tickets):
    """Collect a note and delegate validation to Engineer A."""
    ticket_id = input("Ticket ID: ")
    author = input("Author: ")
    message = input("Note message: ")

    note = add_note(tickets, ticket_id, author, message)
    print(f"Added note {note['note_id']}.")
    return note


def prompt_view_notes(tickets):
    """View notes without modifying the ticket."""
    ticket = _find_ticket(tickets, input("Ticket ID: "))
    notes = ticket.get("notes", [])

    if not notes:
        print(f"No notes for {ticket['id']}.")
        return []

    print(f"\nNotes for {ticket['id']}:")
    for note in notes:
        print(
            f"{note['note_id']} | "
            f"{note['author']}: {note['message']}"
        )

    return notes
