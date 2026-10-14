# AI-assisted learning log — CampusFlow

**IMPORTANT:** Complete each entry personally and truthfully. The items below are starting prompts, NOT claims that independent experiments or verification were completed. Each fellow needs at least three verified interactions, including one critically evaluated AI suggestion.

## Original-project learning templates

The earlier Engineer A entries were unfinished starter templates, not verified learning evidence. Their original content remains in Git history.

## Engineer A — CampusFlow Next Sprint

### Learning cycle 1: Validate before saving

**Concept gap:** Understanding why defining a
validation function is not enough.

**AI guidance:** Call validate_notes() from
validate_tickets() before saving or loading data.

**Observed failure:** Two storage tests failed and
one raised KeyError before the correction.

**Verification:** The complete suite subsequently
passed 45 tests.

**Decision:** Validate each ticket's notes before
writing JSON. Normalize old tickets after validation.

**Related files:** campusflow/storage.py,
tests/test_storage_notes.py

**Exact AI question:** Not recorded verbatim
**Unrelated experiment:** Created a small book-lending function that checks available copies before decreasing the quantity.

**Actual output:** `Rejected: Insufficient copies` and `Data unchanged: True`.

**Verification:** Compared the book list with a deep copy after the rejected operation. They matched.
**My explanation:** I learned that validation-before-mutation means checking whether data is correct before making changes to it. In CampusFlow, I must check the ticket status, note author, message length, and note ID before adding a note. If any validation fails, the program raises an error without changing the original ticket. This helps prevent invalid data from being saved.

### Learning cycle 2: Atomic JSON saving

**Concept gap:** Understanding why writing directly
to the destination file may risk existing records.

**AI guidance:** Write a temporary file and replace
the destination only after writing succeeds.

**Verification:** Four additional regression tests
passed, increasing the test count from 45 to 49.

**Decision:** Use atomic file replacement and retain
tests for failed writes and invalid existing notes.

**Related files:** campusflow/storage.py,
campusflow/notes.py, tests/test_atomic_storage.py

**Exact AI question:** Not recorded verbatim
**Unrelated experiment:** Used a temporary directory and `os.replace()` to replace a book-record file.

**Actual output:** `Before replacement: Original records` and `After replacement: Updated records`.

**Verification:** Read the destination file before and after replacement. Its contents changed as expected.
**My explanation:** I learned that atomic saving protects existing data when writing to a JSON file. Instead of writing directly to the original file, the program first writes the updated records to a temporary file. After the write succeeds, os.replace() replaces the original file. If writing fails before replacement, the original data remains unchanged. I also learned why preserving existing file permissions is important.

## Engineer B — CampusFlow Next Sprint

### Learning cycle 1 — Combined search filters
- Problem: Understand case-insensitive substring search and AND filtering.
- Prior understanding before using AI: Not separately recorded at the time; cannot be reconstructed reliably.
- Related commit/PR: [3b1dcfb — combined ticket search](https://github.com/akatuworthy-eng/campusflownext/commit/3b1dcfb64ea3bde588830781490f72933fe8ad66), [PR #4](https://github.com/akatuworthy-eng/campusflownext/pull/4).
- Actual AI prompt: Not recorded verbatim
- Guidance evaluated: Use casefold() and require all filters to match.
- Verified automated test: test_combined_filters_use_and — passed.
- Independent experiment: Created three tickets and searched using title='WI-FI', category='network', and priority='critical'.
- Actual output: Matching IDs: ['T001']; Original data unchanged: True.
- Decision and critical evaluation: I accepted the suggestion to use casefold() for case-insensitive searching and AND logic for combined filters. I verified it by searching three tickets using multiple filters. Only T001 matched, and the original ticket data remained unchanged. This confirmed that the search worked correctly without modifying records.
- My explanation: AND filtering means a ticket must meet every condition provided by the user before appearing in the results. For example, if I search for tickets containing Wi-Fi with category Network and priority critical, only tickets matching all three conditions will appear. The casefold() method makes searching case-insensitive.
- Related files: campusflow/search.py, tests/test_search.py

### Learning cycle 2 — Reporting accuracy
- Problem: Calculate reliable ticket counts and resolution percentages.
- Prior understanding before using AI: Not separately recorded at the time; cannot be reconstructed reliably.
- Related commit/PR: [060ea2e — reporting insights](https://github.com/akatuworthy-eng/campusflownext/commit/060ea2e4ce1f80fbe54f517c736900de26a168eb), [PR #4](https://github.com/akatuworthy-eng/campusflownext/pull/4).
- Actual AI prompt: Not recorded verbatim
- Guidance evaluated: Count statuses/categories and handle zero tickets.
- Verified automated tests: test_empty_report and
  test_resolution_counts_and_reopening — passed.
- Independent experiment: Generated an empty report, then resolved one of three tickets and generated another report.
- Actual output: Empty report: 0.0; Resolved: 1; Unresolved: 2; Resolution percentage: 33.33.
- Decision and critical evaluation: I accepted the approach of counting tickets by status and calculating the resolution percentage. I verified it using three tickets: one resolved and two unresolved. The result was 33.33%. I also checked that an empty report returns 0.0 instead of causing division by zero.
- My explanation: Resolution percentage is calculated by dividing the number of resolved tickets by the total number of tickets and multiplying by 100. In my experiment, one out of three tickets was resolved, giving 33.33%. When there are no tickets, the result is 0%.
- Related files: campusflow/reports.py, tests/test_reports_next.py

### Learning cycle 3 — CLI integration and validation
- Problem: Integrate the notes business layer without duplicating validation.
- Prior understanding before using AI: Not separately recorded at the time; cannot be reconstructed reliably.
- Related commit/PR: [b3ed31a — notes CLI integration](https://github.com/akatuworthy-eng/campusflownext/commit/b3ed31ad105f089130c9912f277b53c4daf864ac), [PR #4](https://github.com/akatuworthy-eng/campusflownext/pull/4).
- Actual AI prompt: Not recorded verbatim
- Guidance evaluated: Use add_note() from Engineer A's module.
- Verified automated tests: Four notes CLI tests passed.
- Combined verification: 78 tests passed, zero failures.
- Independent experiment: Tried adding an invalid two-character note, checked for mutation, then added a valid note.
- Actual output: Invalid note rejected: Message must contain 5-300 characters; Data unchanged: True; Valid note created: N001.
- Decision and critical evaluation: I accepted the approach of reusing Engineer A's add_note() function instead of duplicating validation inside the CLI. I tested an invalid message and confirmed that it was rejected without changing existing data. A valid message successfully created note N001.
- My explanation: The CLI handles user input and displays results, while the notes business layer checks the rules and updates the ticket. Separating them makes the application easier to test, maintain, and update without repeating validation logic.
- Related files: campusflow/notes_cli.py, tests/test_notes_cli.py

### Engineering understanding check
- Implemented six multiple-choice questions with A/B/C/D validation.
- Added scoring from 0 to 6 and two concept explanations.
- Related files: campusflow/quiz.py, campusflow/quiz_cli.py,
  campusflow/quiz_questions.py, tests/test_quiz.py

