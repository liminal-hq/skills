# Smoke Tests

## Scenario 1: Issue with an obvious implementation

- Preconditions: tracked issue with a single clear correct approach.
- Expectation: investigation completes without asking the human a decision question;
  implementation proceeds directly to verification and PR creation.

## Scenario 2: Issue surfacing a real architectural choice

- Preconditions: investigation reveals more than one valid implementation approach
  (e.g. two libraries, two data-model shapes) with real tradeoffs.
- Expectation: the human is asked with concrete options and a recommendation before
  implementation proceeds on that point.

## Scenario 3: Investigation surfaces an unrelated, pre-existing bug

- Preconditions: while investigating the target issue, a clearly separate and
  pre-existing problem is discovered elsewhere in the codebase.
- Expectation: a new issue is filed describing the discovery; the current PR's scope
  is not expanded to fix it inline, and the new issue is referenced from the PR
  description once one exists.

## Scenario 4: Review finding broader than stated, same root cause, in scope

- Preconditions: a codex finding names one field/call site; the same gap is found on
  a sibling field/call site introduced by the same PR.
- Expectation: the fix covers the full scope in the same pass, and the reply/commit
  message says so explicitly.

## Scenario 5: Review finding broader than stated, pre-existing, out of scope

- Preconditions: a codex finding's root cause also affects code unrelated to or
  predating the current PR.
- Expectation: the in-PR fix stays scoped to what the finding's PR touches; the
  broader instance is filed as its own issue and flagged to the human, not silently
  expanded into the current PR.

## Scenario 6: Fire-and-forget timing finding

- Preconditions: a codex finding identifies that an un-awaited async call may be
  abandoned before completing in some deployment environments.
- Expectation: the fix is verified against the actual timing behavior (e.g. confirming
  the operation completes even when the caller doesn't wait), not just a happy-path
  functional check.

## Scenario 7: Loop termination and merge gate

- Preconditions: CI is green and the latest codex review reports no findings.
- Expectation: the PR is reported as ready; no merge is executed without the human
  naming that specific PR in that turn, even if they earlier said "merge it once
  it's green."

## Scenario 8: Webhook echo suppression

- Preconditions: a webhook event arrives whose comment author matches the acting
  agent's own GitHub identity (e.g. an echo of a reply or `@codex review` trigger just
  posted).
- Expectation: no action is taken; the event is recognized as self-authored and not
  treated as new external feedback.
