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
TODO: Add the specific findings from our original audit.

## Engineer A improvement evidence
- Added structured follow-up notes.
- Added note validation and ID continuity.
- Preserved compatibility with older tickets.
- Added atomic JSON saving and regression tests.
- Latest local test run: 49 passed, 0 failed.

## Remaining baseline verification
TODO: Record three manual CLI input/output checks
if required by the mentor.
