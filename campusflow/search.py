"""Read-only search and filtering for CampusFlow tickets."""

CATEGORIES = ("network", "hardware", "software", "other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def normalize_filter(value, name, allowed=None):
    """Validate and normalize an optional search filter."""
    if value is None:
        return ""

    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")

    value = value.strip().casefold()

    if value and allowed is not None and value not in allowed:
        raise ValueError(f"Invalid {name}: {value}")

    return value


def search_tickets(
    tickets,
    title="",
    category="",
    status="",
    priority="",
    sort_by_priority=False,
):
    """Return tickets matching ALL supplied filters."""

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be a list")

    title = normalize_filter(title, "title")
    category = normalize_filter(category, "category", CATEGORIES)
    status = normalize_filter(status, "status", STATUSES)
    priority = normalize_filter(priority, "priority", PRIORITIES)

    results = []

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Invalid ticket record")

        if title and title not in ticket["title"].casefold():
            continue

        if category and category != ticket["category"].casefold():
            continue

        if status and status != ticket["status"].casefold():
            continue

        if priority and priority != ticket["priority"].casefold():
            continue

        results.append(ticket)

    if sort_by_priority:
        results.sort(
            key=lambda ticket: (
                PRIORITY_ORDER[ticket["priority"]],
                int(ticket["id"][1:]),
            )
        )

    return results
