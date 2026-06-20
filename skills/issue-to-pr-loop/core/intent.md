# Intent

`issue-to-pr-loop` drives a single tracked issue from investigation through to a
merge-ready pull request: research the real scope, surface architecture decisions to
the human instead of guessing, implement with empirical verification built in from the
start, open the PR with house conventions, then run repeated rounds of automated review
until clean — fixing every finding by reproducing the bug first, not by inference.

## Objectives

- **Investigate before implementing.** Read the issue, the actual current code (not
  assumptions about it), and the relevant library/framework internals when the issue
  touches a third-party system's behavior. Confirm claims empirically — by reading
  source, running a small script, or testing against a real instance — before treating
  them as fact.
- **Surface real decisions instead of guessing.** When the issue or its investigation
  surfaces a genuine architectural choice (which of two valid approaches, what to do
  with a pre-existing related gap discovered along the way, whether to expand scope),
  ask the human with concrete options and a recommendation — don't pick silently and
  don't ask about things that have an obvious correct answer.
- **Build verification into implementation, not after it.** As each piece lands, prove
  it does what it claims — reproduce the failure mode the issue describes, confirm the
  fix addresses it, check adjacent flows for regressions — rather than writing code and
  trusting it.
- **Spin off out-of-scope discoveries as new tracked issues**, not as scope creep on
  the current PR. If investigation or review surfaces a real problem that is bigger
  than, unrelated to, or merely adjacent to the one being worked, file it (with enough
  detail to act on later) and reference it from the current PR rather than fixing it
  inline or silently dropping it.
- **Open the PR following house convention**, then drive it through repeated rounds of
  automated review until clean (see "Review loop" below), reproducing every finding
  before fixing it.
- **Stop short of merging.** Report the PR as ready and wait for the human to name that
  specific PR for merge, even after an earlier "merge it once it's green" statement.

## Non-goals

- Multi-PR batch ordering, conflict detection across PRs, or integration-branch
  orchestration — that is `pr-integration`'s job.
- Autonomous merging under any circumstance.
- Silently expanding the current PR's scope to absorb every discovery made along the
  way — small, same-root-cause fixes within the PR's existing diff are fine; unrelated
  or much-larger problems get their own issue instead.
- Patching a review finding's literal wording without checking whether the same root
  cause exists elsewhere in the codebase.

## Review loop (sub-phase)

Once a PR is open, this skill also covers driving it through repeated codex review
rounds — see `workflow.md`'s "Review loop" section. This sub-phase can also be entered
directly (without the investigation/implementation phases) when asked to "watch",
"check on", or "finish off" an already-open PR.
