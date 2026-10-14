"""Reporting helpers for CampusFlow tickets."""

STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")
CATEGORIES = ("Network", "Hardware", "Software", "Other")


def generate_report(tickets):
    """Return current ticket counts and resolution insights."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list")

    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}
    by_category = {category: 0 for category in CATEGORIES}

    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")
        category = ticket.get("category")

        if status in by_status:
            by_status[status] += 1

        if priority in by_priority:
            by_priority[priority] += 1

        if category in by_category:
            by_category[category] += 1

    total = len(tickets)
    resolved = by_status["resolved"]
    unresolved = (
        by_status["open"] + by_status["in_progress"]
    )

    resolution_percentage = (
        resolved / total * 100 if total else 0.0
    )

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_percentage": resolution_percentage,
    }
