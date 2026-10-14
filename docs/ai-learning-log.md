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

## Engineer B
Create three separate genuine entries following the same fields: problem, prior understanding, exact AI prompt, guidance, independent experiment, actual verification, decision, related commit/PR, and your own explanation.
