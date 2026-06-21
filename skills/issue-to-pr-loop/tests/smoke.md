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

## Scenario 9: Comment pagination on a long review loop

- Preconditions: a PR has accumulated more than 30 review comments (top-level and/or
  inline) across multiple review rounds, spanning more than one API page.
- Expectation: the latest top-level summary comment and all unresolved inline
  findings are correctly identified across every page — not truncated to the first
  30-comment page in ascending order.

## Scenario 10: Selecting the latest comment across multiple pages

- Preconditions: same multi-page PR as Scenario 9, specifically selecting "the latest
  top-level comment" by position (`.[-1]`-style logic).
- Expectation: the selection uses `--paginate --slurp` aggregated through an external
  `jq 'add | .[-1]'`, not `gh api`'s own `--jq` flag with `--paginate` — confirmed by
  checking the selected comment's `id`/`created_at` actually matches the true latest
  comment across the full PR, not merely the last item of whichever page `gh api`
  happened to process last.

## Scenario 11: Latest-comment selection ignores non-bot comments

- Preconditions: a PR where the reviewing bot posted a clean summary, and a human
  (or another bot/status integration) posted a comment afterward.
- Expectation: the "latest review comment" selection filters to the reviewing bot's
  login before taking the last item, correctly returning the bot's clean summary —
  not the later human/other-bot comment.

## Scenario 12: Fixed findings don't block on isResolved

- Preconditions: a PR where every finding from a review round has been fixed and
  replied to in-thread, but the resolve-thread step from "Commit and push" was
  skipped.
- Expectation: the status check still correctly reports zero unresolved findings,
  because "unresolved" is determined by the has-a-reply-yet check (a root comment
  with no reply), not by `isResolved` — which would incorrectly show every thread as
  still open in this scenario, confirmed empirically on a real merged PR where this
  step had never been performed.

## Scenario 13: Threads get resolved after replying

- Preconditions: a finding has just been fixed, verified, and replied to in-thread.
- Expectation: before requesting a fresh review, the thread's `resolveReviewThread`
  mutation is called (using the thread's GraphQL node ID), and the thread's
  `isResolved` field reads `true` afterward — keeping the PR's "Files changed" view
  uncluttered with addressed items for human reviewers, independent of how this
  skill's own automation determines "unresolved."

## Scenario 14: Resolving a thread requires the GraphQL thread ID, not a REST ID

- Preconditions: a finding has been fixed and replied to via the REST review-comment
  reply endpoint; the only IDs on hand so far are from the REST `pulls/<N>/comments`
  response used in status-check step 3 (a `PullRequestReviewComment` `id`/`node_id`).
- Expectation: before calling `resolveReviewThread`, the `reviewThreads` GraphQL query
  (status-check step 4) is run and the finding's root comment is matched to its
  thread by `databaseId`, yielding the thread's own node `id`. Passing the REST
  comment's `node_id` directly to `resolveReviewThread`'s `threadId` input is not
  attempted — it is the wrong GraphQL object type and the mutation would fail.

## Scenario 15: Clean summary predates the latest push

- Preconditions: codex posted a clean "Didn't find any major issues" summary
  reviewing commit `abc1234`. After that, a new commit `def5678` was pushed (e.g. an
  unrelated fix prompted by a different inline finding in the same round), and no
  fresh codex summary has arrived yet by the time of the next status check.
- Expectation: the status check extracts `abc1234` from the summary's `**Reviewed
  commit:**` line, compares it against the PR's current `headRefOid` (`def5678`),
  finds a mismatch, and does **not** treat the PR as codex-clean — CI being green and
  no new inline findings existing yet does not change this. The loop re-requests
  review and keeps waiting rather than reporting the PR ready off a stale clean
  verdict.

## Scenario 16: `gh api` placeholder substitution

- Preconditions: an agent runs any `gh api repos/...` call from the status-check or
  per-finding sequence, either against the current directory's repository or an
  explicitly different one.
- Expectation: the endpoint path uses `{owner}`/`{repo}` (the only placeholders `gh
  api` substitutes, confirmed via `gh help api` and a direct repro: `gh api
  repos/:owner/:repo/pulls/<N>` 404s, since `:owner`/`:repo` are sent as literal path
  segments) — never Octokit-style `:owner`/`:repo`. For GraphQL calls (`gh api
  graphql -f query=...`), `{owner}`/`{repo}` are not substituted inside the query
  string at all (confirmed via a direct repro returning `Could not resolve to a
  Repository with the name '{owner}/{repo}'`); the real owner/repo are passed as
  GraphQL variables via `-f`/`-F` instead.

## Scenario 17: A non-agent reply does not clear a finding

- Preconditions: a codex finding's root comment has exactly one reply, and that
  reply is from a human asking a clarifying question (or from codex itself
  following up), not from the acting agent confirming a fix.
- Expectation: the status check's unresolved-findings query, filtered to the
  acting agent's own login (`gh api user -q .login`), still reports this root
  comment as unresolved — confirmed directly: a root comment replied to only by
  `chatgpt-codex-connector[bot]` is correctly still flagged by the
  `$actor`-filtered query, where an unfiltered "any reply exists" query would
  have incorrectly cleared it. The loop does not skip reproducing/fixing this
  finding on the basis of that reply.

## Scenario 18a: A later non-agent reply reopens a finding

- Preconditions: a codex finding's root comment has two replies in order: first
  the agent's fix-reply citing a commit, then a later reply from codex (or a
  human reviewer) saying the fix is still insufficient.
- Expectation: the status check's unresolved-findings query reports this root
  comment as unresolved again, because it checks the **latest** reply's author,
  not merely whether the agent has replied at any point in the thread — confirmed
  directly with a synthetic three-comment thread (root → agent's fix-reply →
  codex's later "still not fixed" reply): the latest-reply-by-`created_at` check
  correctly flags it unresolved, where a check that only asked "has the agent
  ever replied to this root" would have incorrectly left it cleared. The loop
  re-investigates this finding rather than reporting the PR ready.

## Scenario 18: Echo suppression doesn't stall an external event

- Preconditions: the agent has just replied to several findings in a round, so the
  latest *inline* review comment on the PR is the agent's own reply. A genuinely
  new, external event then arrives — e.g. a fresh top-level codex summary
  reporting new findings, or a CI-failure webhook.
- Expectation: the status check still acts on the new external event. Echo
  suppression is evaluated against the specific triggering event's author, not
  against "is the latest item in the inline (or top-level) stream self-authored" —
  the latter would incorrectly skip the entire status check merely because the
  agent's own prior reply happens to currently be the latest inline comment.
