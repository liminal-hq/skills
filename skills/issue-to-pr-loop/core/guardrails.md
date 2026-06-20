# Guardrails

## Required Gates

1. The issue (or PR description, if entering at the review-loop phase) has been read
   in full before any code is written.
2. Claims about third-party library/framework behavior driving the implementation
   have been confirmed empirically (source read, script run, or live test), not
   assumed from memory.
3. Any genuine architectural decision surfaced during investigation has been put to
   the human with concrete options, before implementation proceeds on that point.
4. Any out-of-scope discovery (bigger, unrelated, or merely adjacent to the task) has
   been filed as its own tracked issue rather than folded into the current PR.
5. Every meaningful implementation piece has been verified against the failure mode it
   addresses, not just covered by a passing unit test.
6. Every review finding has been read in full, not just its title/badge.
7. Every review finding has been reproduced before being marked fixed — no patch lands
   without first confirming the underlying bug actually manifests as described.
8. Every fix has been re-verified against the same reproduction, confirming the bug no
   longer occurs.
9. Every fix has been checked against other call sites for the same root cause.
10. Full local validation suite passes after each fix (typecheck, lint, tests, plus any
    project-specific gates such as migration/seed round-trips).
11. Every review finding has an in-thread reply (not a new top-level comment) citing
    the fixing commit and the verification evidence.
12. Every replied-to finding's review thread has been explicitly resolved via the
    `resolveReviewThread` GraphQL mutation — posting a reply does not do this
    automatically, and it does not happen on its own just because the underlying code
    was fixed.
13. A fresh review has been requested after all replies for a round are posted.
14. Backticks wrap every identifier, path, and command in commit messages and PR
    replies.

## Safety Rules

- Never merge without the human naming that specific PR in that turn, even after an
  advance statement like "merge it once green."
- Never rewrite already-pushed commit history (reword, squash, force-push) without the
  human's explicit confirmation for that specific rebase, even if a similar cleanup was
  discussed earlier in the same conversation — confirm again right before executing it,
  since "leave it for now" and "fix it later" are easy to conflate across a long thread.
- Do not act on a webhook event that is the echo of your own reply or your own
  review-trigger comment (author matches your own GitHub identity).
- Do not patch around a finding's literal wording without checking whether the same
  root cause exists elsewhere — a finding scoped to one field is often a symptom of a
  gap that exists on several fields.
- If reproduction reveals the bug is broader than the finding states and the broader
  instance is pre-existing on the target branch (not introduced by the current PR) or
  otherwise substantially out of scope, file it as its own tracked issue and surface
  it explicitly to the human, rather than silently expanding the current PR's scope.
- Keep CI-green and codex-clean separate concepts: CI passing does not mean codex has
  reviewed the latest commit; codex being silent does not mean it has finished — check
  the latest reviewed commit SHA in its summary comment against your last push.
- A fix that changes timing/ordering assumptions (fire-and-forget vs. awaited,
  synchronous vs. async dispatch) needs its own explicit verification of the new
  timing behavior, not just a check that the happy path still produces the right
  end-state — the previous review round's regression check is about *correctness*,
  this one is about *whether the operation is guaranteed to run at all* in the
  target deployment environment.
- Always pass `--paginate` on `gh api` list calls for PR/issue comments, and when
  selecting a single item by position (e.g. `.[-1]` for "the latest comment"), use
  `--paginate --slurp` piped to an external `jq 'add | ...'` rather than `gh api`'s own
  `--jq` flag. GitHub's REST API defaults to `per_page=30`/page 1 in ascending order,
  so an unpaginated call returns the 30th *oldest* comment via `.[-1]`, not the
  latest. `--paginate` alone is not sufficient either: `gh api`'s `--jq` runs once per
  page, not once over the combined result, so `--paginate --jq '.[-1]'` across N pages
  prints N separate "last comments" — reading the wrong one (e.g. the first line) is
  an easy mistake that silently treats a stale page-ending comment as current.
  `--slurp` aggregates all pages into one array first, but `gh api` forbids combining
  `--slurp` with its own `--jq`, hence the external-`jq` pipe. Position-independent
  filters (`select(...)`) are safe to apply per-page without aggregation, since the
  union of per-page results is still correct — only positional indexing needs the
  full aggregate first. This becomes routine, not an edge case, on any review loop
  that runs more than a few rounds.
- When selecting "the latest top-level review comment," filter to the codex bot's
  login (or whatever review bot is in use) before applying positional indexing — the
  issue-comments endpoint returns every conversation comment on the PR, not just the
  reviewing bot's, so any later human reply, status comment, or other bot's comment
  would otherwise be selected instead of the bot's actual last verdict.
- Disagreeing with a finding requires the same empirical rigor as agreeing with one.
  A well-reasoned finding can still fail to reproduce in a specific project's actual
  configuration (confirmed directly: a finding about an unresolvable TypeScript
  import breaking CI was structurally correct in general, but didn't reproduce in a
  true fresh-checkout test because the target project already had `skipLibCheck:
  true`, which happens to suppress that exact error class for declaration files).
  When a finding doesn't reproduce, say so with the specific evidence (the exact
  reproduction attempted and its result), not a bare disagreement — and acknowledge
  explicitly that the underlying reasoning would be a real risk under a different
  configuration.
- The `resolveReviewThread` GraphQL mutation requires `pull-requests: write`
  permission (covered by a personal-access-token's `repo` scope, but not necessarily
  by a fine-grained PAT or CI service token without that explicit grant) — confirm
  this is available before relying on the resolve-thread step succeeding silently.

## Rollback

If a fix introduces a regression discovered during the post-fix validation pass:

1. Do not push the broken commit.
2. Fix the regression in the same commit (amend, since it has not been pushed yet) or
   add a follow-up commit if the regression was found after a push.
3. Re-run the full validation suite before proceeding.
