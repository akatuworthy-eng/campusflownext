# CampusFlow Next — Final Engineering Audit Readiness

**Prepared:** 14 October 2026  
**Scope:** Completed work on Engineer A and Engineer B feature branches.  
**Status:** Feature-complete and locally tested; **not yet formally merged or peer-approved**.

## Pull requests and branch layout

| PR | Branch | Base | Current status |
| --- | --- | --- | --- |
| [#3 — Engineer A](https://github.com/akatuworthy-eng/campusflownext/pull/3) | `feat/21-validation-and-notes` | `main` | Open; `Ragi232` review requested; no submitted human approval |
| [#4 — Engineer B](https://github.com/akatuworthy-eng/campusflownext/pull/4) | `feat/22-search-and-insights` | `feat/21-validation-and-notes` | Open; no requested reviewer or submitted human approval |

**Identity/review limitation:** GitHub currently attributes **both PRs** to `akatuworthy-eng`, so that account cannot approve either PR. A technical audit or self-comment is not a substitute for each engineer's genuine review. If reciprocal formal approvals are required, the team must resolve the PR author/reviewer arrangement with the mentor or GitHub account owners. Do not claim reciprocal review has occurred when it has not.

## Work implemented

### Engineer A — Issue #1
- Ticket creation and priority rules, with validation and canonical sequential ticket IDs.
- Structured follow-up notes: `add_note(tickets, ticket_id, author, message)`, `N001+` IDs, author and 5–300-character message validation, no notes on resolved tickets until reopening.
- Storage validation of tickets, note structures and IDs, corrupt/duplicate JSON rejection, normalization of legacy tickets missing `notes`.
- Atomic JSON saving using a temporary file and `os.replace()`; replacement preserves mode bits of an existing destination file.
- Regression tests for invalid operations, ID sequences, data preservation and permissions.

### Engineer B — Issue #2
- Read-only ticket search: case-insensitive title substring, category/status/priority filters combined with AND, and optional priority ordering.
- CLI search, with invalid-filter retry and ticket/assignee display.
- Reports: status, priority, category, resolved/unresolved counts and percent resolved; safe empty-data behavior.
- Six-question engineering understanding quiz: A/B/C/D validation, score 0–6, two explanations.
- Notes CLI: add and view follow-up notes, delegating business validation to Engineer A's API.
- Tests for search, reports, quiz and notes CLI, including rejected note input and reopening.

## Verification evidence — observed terminal results

| Stage | Tests reported | Result |
| --- | ---: | --- |
| Original CampusFlow baseline | 37 | PASS |
| Latest isolated Engineer A branch, independently run from Engineer B's review worktree | 52 | PASS (historical local) |
| Combined branches before notes CLI integration | 74 | PASS |
| Combined branch with notes CLI and four integration tests | 78 | PASS, zero failures (historical local) |
| Updated Engineer A branch, GitHub Actions on Linux and Windows, Python 3.11 | 54 | PASS on both systems |
| Updated Engineer B combined branch, GitHub Actions on Linux and Windows, Python 3.11 | 82 | PASS on both systems |

**Most recent reported command:** `python3 -m unittest discover -s tests -q`. Engineer B's terminal showed `Ran 78 tests ... OK` after integration and before the final docs-only commits. GitHub Actions now runs the regression suite on Linux and Windows for both feature branches. Successful workflow runs verified: [Engineer A tests](https://github.com/akatuworthy-eng/campusflownext/actions/runs/38637795572) (54 tests) and [Engineer B tests](https://github.com/akatuworthy-eng/campusflownext/actions/runs/38637811790) (82 tests). A later branch-reconciliation commit may require its own check result before merging. Earlier counts of 52 and 78 are historic local test results, not current suite totals.

### Engineer B independent experiments

1. **Combined search:** Three tickets, search for `WI-FI` + `network` + `critical` returned `['T001']`; `Original data unchanged: True`.
2. **Reporting:** An empty report returned `0.0`; after resolving one of three tickets: `Resolved: 1`, `Unresolved: 2`, `Resolution percentage: 33.33`.
3. **Notes:** `Hi` rejected with `Message must contain 5-300 characters`; `Data unchanged: True`; a valid note produced `N001`.

The learning log records three Engineer B learning cycles and Engineer A experiments. Original exact AI question wording is marked **Not recorded verbatim** wherever it was not preserved; never substitute invented quotations. The original baseline also marks independent manual CLI verification as outstanding.

## Demonstration script for the audit

1. Create two tickets with different categories, urgency and affected-user counts; explain how `calculate_priority()` selects the priority.
2. Try creating an invalid/blank title; verify no ticket is added.
3. Assign a ticket, start progress and resolve it; show why illegal transitions are rejected.
4. Add a 5–300-character follow-up note to an open ticket, display it, save/restart and confirm the ID and note survive reload.
5. Try adding a short note and a note to a resolved ticket; verify rejection, then reopen and add a valid note.
6. Search by mixed-case title plus multiple filters; show AND matching and no mutation.
7. Display reports before and after resolution/reopening; explain `resolved / total × 100` and zero-ticket handling.
8. Run the six-question quiz and demonstrate invalid-answer retries.
9. Run `python3 -m unittest discover -s tests -v` and explain at least one test for validation, storage, search and CLI integration.

Use a **temporary ticket JSON file** for the live demo to protect real records.

## Open items before claiming the repository is finalized

- [ ] Genuine Engineer B review/approval of PR #3 is recorded if required by the program.
- [ ] Genuine Engineer A review/approval of Engineer B's changes is recorded if required; both PRs currently being attributed to one account is an unresolved workflow obstacle.
- [ ] Reviewer checks that all review comments are addressed. A possible workflow invariant requiring investigation: does a `resolved` ticket also need a nonblank assignee on load?
- [ ] Confirm the mentor's minimum learning-evidence requirements, especially exact AI prompts that were not recorded.
- [ ] Perform and record independent manual CLI verification if required. Automated CLI tests do not constitute a human manual run.
- [ ] Merge PR #3 into `main` **after review**.
- [ ] Retarget PR #4 to `main` after PR #3 merges, confirm it shows only Engineer B's changes, rerun tests, and merge **after review**.
- [ ] Verify `main` contains the complete application and repeat tests from a clean checkout.

## Suggested questions for oral defense

- Why use `casefold()` instead of just comparing raw title strings?
- Why do combined search filters use AND?
- How is searching read-only if it returns ticket dictionaries?
- What happens when the number of resolved tickets is zero or the list is empty?
- Why should validation run before mutating a ticket?
- Why does writing to a temporary file before `os.replace()` protect the original data?
- How do you avoid duplicating note-validation logic in the CLI?
- How do you prove your code did not break the original 37 tests?

## Recommended merge sequence

1. Secure required review on PR #3, then merge PR #3 into `main`.
2. Retarget PR #4 from `feat/21-validation-and-notes` to `main`.
3. Verify the PR #4 diff and test results, secure its required review, then merge it.
4. Re-run the complete suite against updated `main` and record the result.

**Implementation review notes:** Engineer A's unresolved-assignee storage rule now also rejects unassigned resolved records; Engineer B's search returns detached snapshots, reporting rejects invalid values, and README documents all 13 CLI actions. Both branches contain a GitHub Actions workflow.

**Do not mark a review, check or merge as done unless GitHub and actual testing confirm it.**
