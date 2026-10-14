# CampusFlow Next

A Python standard-library command-line helpdesk ticket manager with validated ticket workflows, structured follow-up notes, search, reporting, and an engineering understanding quiz. Ticket data is stored locally in JSON.

## Run the application

Run from the repository root:

```bash
python3 main.py
```

On Windows, use `py main.py`.

The program loads `data/tickets.json` on startup. If it does not exist, the application starts empty. Selecting Save or Exit writes validated tickets. Malformed or invalid stored data causes a safe startup error instead of replacing the original file.

## Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

On Windows, use `py -m unittest discover -s tests -v`. The GitHub Actions workflow runs the same suite on Linux and Windows.

## CLI menu

| Option | Action |
| --- | --- |
| 1 | Create ticket |
| 2 | List tickets |
| 3 | View a ticket |
| 4 | Assign a ticket |
| 5 | Change status (enter `reopen` to reopen a resolved ticket) |
| 6 | Show the open work queue |
| 7 | Show reports |
| 8 | Save tickets |
| 9 | Exit (saves tickets) |
| 10 | Search tickets |
| 11 | Engineering understanding check |
| 12 | Add a follow-up note |
| 13 | View follow-up notes |

## Ticket rules

- Categories: Network, Hardware, Software, Other.
- Urgency levels: low, medium, high.
- Priority (highest rule takes precedence):
  1. High urgency **and** 10 or more affected users → `critical`.
  2. High urgency **or** 10 or more affected users → `high`.
  3. Medium urgency **or** 3 or more affected users → `medium`.
  4. Otherwise → `low`.
- Workflow: `open` → `in_progress` → `resolved`; starting progress requires a nonblank assignee. Reopening a resolved ticket requires the explicit `reopen` action. Storage also requires an assignee for `in_progress` and `resolved` records.
- The open work queue remains sorted by priority, then numeric ticket ID; search sorting is separate and never rearranges the work queue.

## Follow-up notes

- Add notes only to `open` or `in_progress` tickets. Reopen a `resolved` ticket first.
- Authors must be nonblank. Note messages are trimmed and must contain **5–300 characters**.
- Notes have sequential per-ticket IDs such as `N001`, `N002`; IDs continue after saving and reloading.
- Legacy ticket JSON without a `notes` field loads with an empty note list.
- Invalid notes and storage data are rejected before modification.

## Search and reports

- Title search is case-insensitive and matches substrings, using Unicode `casefold()`.
- Category, status and priority filters are optional; **all supplied filters must match** (AND).
- Invalid filter choices are re-prompted. Optional priority sorting orders only returned search results.
- Searching does not modify stored records; its returned dictionaries are detached snapshots.
- Reports show totals by status, priority and category, resolved and unresolved counts, and the percentage resolved. Empty-data resolution is `0.00%`.
- Reporting rejects invalid statuses, priorities and categories rather than silently skewing totals.

## Engineering understanding check

Option 11 asks six multiple-choice questions, accepts only A/B/C/D (re-prompting invalid answers), scores from 0 to 6, and displays two concept explanations.

## Reliability and limitations

JSON saving validates the data, writes to a temporary file in the destination directory, flushes it, then atomically replaces the destination. Existing file mode bits are preserved on replacement; new files use a private temporary-file mode. This protects against many failed-write scenarios but is **not** a full transactional database or a multi-process concurrent editing system.

CampusFlow Next does **not** include user authentication, multi-user conflict handling, or a graphical/web UI. Its CLI operates on one local JSON file at a time.

## Development, reviews and audit

- [Engineer A — PR #3](https://github.com/akatuworthy-eng/campusflownext/pull/3): validation, notes and storage.
- [Engineer B — PR #4](https://github.com/akatuworthy-eng/campusflownext/pull/4): search, reporting, quiz and CLI integration.
- [Audit readiness and demonstration plan](docs/audit-readiness.md).
- [Engineering design decisions](docs/design-decisions.md).
- [AI-assisted learning evidence](docs/ai-learning-log.md).

Passing local tests does not replace required independent code-review approvals. Merge PR #3 into `main` first after review; then retarget PR #4 to `main`, re-verify and merge after review.
