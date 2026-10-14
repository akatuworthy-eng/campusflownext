"""Interactive search interface for CampusFlow."""

from campusflow.search import (
    CATEGORIES,
    STATUSES,
    PRIORITIES,
    normalize_filter,
    search_tickets,
)


def ask_filter(name, prompt, allowed=None):
    """Keep asking until an optional filter is valid."""
    while True:
        value = input(prompt)
        try:
            return normalize_filter(value, name, allowed)
        except ValueError as error:
            print(f"Error: {error}. Please try again.")


def prompt_search_tickets(tickets):
    """Collect filters and display matching tickets."""

    print("\n--- Search Tickets ---")
    print("Press Enter to skip any filter.")

    title = ask_filter("title", "Title contains: ")
    category = ask_filter(
        "category", "Category: ", CATEGORIES
    )
    status = ask_filter(
        "status", "Status: ", STATUSES
    )
    priority = ask_filter(
        "priority", "Priority: ", PRIORITIES
    )
    sort_choice = ask_filter(
        "sorting",
        "Sort by priority? (y/n, Enter = no): ",
        ("y", "n"),
    )

    results = search_tickets(
        tickets,
        title=title,
        category=category,
        status=status,
        priority=priority,
        sort_by_priority=(sort_choice == "y"),
    )

    if not results:
        print("No matching tickets.")
        return results

    print(f"Found {len(results)} ticket(s):")

    for ticket in results:
        assigned = ticket["assigned_to"] or "Unassigned"
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"{ticket['category']} | {ticket['priority']} | "
            f"{ticket['status']} | Assigned: {assigned}"
        )

    return results
