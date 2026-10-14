# CampusFlow Next — Baseline Check

## Original project
Repository: akatuworthy-eng/campusflow-team-01
Original main commit: 8ab4e4278fae1e7d1ea9c31cd9fa40239f8b701c

## Test command
python3 -m unittest discover -s tests -v

## Original baseline results
Tests executed: 37
Passed: 37
Failed: 0
Result: OK

## Three tested input scenarios

### 1. Priority calculation
Input: urgency=high, affected_users=12
Expected: critical priority
Result: Passed automated test.

### 2. Invalid status transition
Input: Move an unassigned open ticket to in_progress.
Expected: Reject the transition.
Result: Passed automated test.

### 3. Duplicate ticket IDs
Input: Load JSON containing duplicate ticket IDs.
Expected: Reject the file.
Result: Passed automated test.

## Audit improvement priorities
The CampusFlow Next brief identifies:
- Stronger validation
- Structured follow-up notes
- Safe JSON storage
- Combined ticket search
- Improved reporting
- Automated tests and peer review

Actual original audit observations:
The available baseline evidence confirms that the original automated tests checked priority calculation, invalid workflow transitions, and duplicate ticket IDs. The separate original audit observations were not provided in this document, so no additional findings are claimed.

## Engineer A improvement evidence
- Added structured follow-up notes.
- Added note validation and ID continuity.
- Preserved compatibility with older tickets.
- Added atomic JSON saving and regression tests.
- Latest Engineer A local test run: 52 passed, 0 failed (including three review-fix tests).

## Remaining baseline verification
The three scenarios recorded above were verified through automated tests, not independent manual CLI sessions. Manual CLI verification remains outstanding.
