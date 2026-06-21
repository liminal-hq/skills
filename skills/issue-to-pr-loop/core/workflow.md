# Workflow

## Phase 1: Investigate

1. Read the issue in full, including any linked context. Don't start coding from the
   title alone.
2. Read the actual current code the issue touches — don't reason from memory of what
   the code probably does.
3. When the issue's premise depends on a third-party library or framework's behavior,
   confirm it empirically: read the library's source in `node_modules` (or equivalent),
   run a small script against it, or test against a real running instance. Don't trust
   a recollection of how a framework "usually" works — versions and configurations
   differ, and being wrong here compounds into the implementation.
4. If investigation surfaces a genuine architectural decision (more than one valid
   approach, a pre-existing related gap, a question of scope), stop and ask the human
   with concrete options and a recommendation. Don't ask about things with an obvious
   correct answer, and don't silently pick for things that aren't obvious.
5. If investigation surfaces a real problem that is bigger than, unrelated to, or only
   adjacent to the issue at hand, do not fold it into the current work. File it as its
   own tracked issue with enough detail to act on later (what's wrong, why, where it
   was discovered), and reference it from the current PR's description once one
   exists. Only fix it inline if it's a small, same-root-cause variant of the thing
   already being changed.

## Phase 2: Implement with verification built in

1. Implement the change.
2. For each meaningful piece, prove it does what it claims before moving on:
   reproduce the failure mode the issue describes against the unpatched code path (if
   feasible) or otherwise demonstrate the fix's effect directly — a script call, a
   curl request, a real browser walkthrough — not just a passing unit test, since
   tests only catch what they were written to catch.
3. Check adjacent flows that touch the same code/data for regressions before
   considering the piece done.
4. Run the project's full local validation suite (typecheck, lint, unit tests, plus
   any project-specific checks such as a seed script or migration round-trip when the
   change touches schema or fixture data) before committing.
5. Commit each logical unit separately, Conventional Commits style, with a body that
   explains why and how it was verified, not just what changed.

## Phase 3: Open the PR

1. Push the branch and open the PR following the project's house conventions (title
   format, `Closes #N` linkage, labels, milestone, review-bot trigger comment such as
   `@codex review`).
2. If any out-of-scope issues were filed during investigation or implementation,
   reference them in the PR description so reviewers have the full picture.
3. Proceed directly into the review loop (Phase 4) — don't wait for a separate
   instruction once the PR is open.

## Phase 4: Review loop

### Trigger conditions

Continue or re-enter this loop when:

- A PR from Phase 3 is open and awaiting review.
- Explicitly asked to watch, check, or finish off a specific already-open PR (this
  phase can be entered directly, skipping Phases 1-3, for that case).
- A `codex_review` or CI-failure webhook event arrives for a PR already being tracked.
- A scheduled check-in fires for a PR with no resolution yet.

### Status check

**`gh api` only substitutes the literal placeholders `{owner}`, `{repo}`, and
`{branch}`** (populated from the current directory's repository, or `GH_REPO`) —
Octokit-style `:owner`/`:repo` colon placeholders are sent through unchanged and
404, since `gh api` has no special handling for them. Every `gh api repos/...` call
below uses `{owner}`/`{repo}`; if running against a repo other than the current
directory's, substitute the real `owner/repo` directly instead.

1. `gh pr checks <N>` for CI state.
2. `gh api --paginate --slurp repos/{owner}/{repo}/issues/<N>/comments | jq 'add | map(select(.user.login == "chatgpt-codex-connector[bot]")) | .[-1]'`
   for the latest *codex* review summary (codex posts a summary comment per pass;
   "Didn't find any major issues" or a 👍 reaction means clean). **Filter to the
   codex bot's login before selecting `.[-1]`** — the issue-comments endpoint returns
   every top-level PR conversation comment, not just codex's, so any later human
   follow-up, status comment, or other bot's comment would otherwise be selected
   instead, and the loop would miss codex's actual last verdict or stall reporting
   the wrong state. **Always pass `--paginate`, and pipe through external `jq`
   rather than `gh api`'s own `--jq`** — GitHub's REST API defaults to
   `per_page=30`/page 1 in ascending order, so on a PR with more than 30 top-level
   comments an unpaginated call returns the 30th *oldest* comment via `.[-1]`, not
   the latest one. `--paginate` alone doesn't fix this either: `gh api`'s own `--jq`
   flag is documented to run once *per page*, not once over the combined result, so
   `--paginate --jq '.[-1]'` across N pages prints N separate "last comments," one
   per page — picking the wrong one (e.g. by reading only the first line) silently
   treats a stale page-ending comment as current. `--slurp` wraps every page into
   one array first; `gh api` forbids combining `--slurp` with its own `--jq`, so
   aggregate with `--slurp` and filter with an external `jq` instead, as shown above.
   **A clean summary is only meaningful if it reviewed the current head.** A clean
   codex summary (e.g. "Codex Review: Didn't find any major issues") names the
   commit it reviewed in a `**Reviewed commit:** \`<short-sha>\`` line in the comment
   body. Extract that short SHA and compare it (prefix match) against
   `gh pr view <N> --json headRefOid -q .headRefOid` — a clean summary for an older
   commit means nothing has reviewed whatever was pushed since, and the loop must
   not treat the PR as clean on that basis alone. This matters most right after a
   push: codex's webhook-triggered review and CI's completion are both typically
   asynchronous relative to the push, so the most recent comment at the moment of a
   status check can easily predate the latest commit.
3. `gh api --paginate --slurp repos/{owner}/{repo}/pulls/<N>/comments | jq 'add | (map(select(.in_reply_to_id != null)) | map(.in_reply_to_id)) as $repliedTo | map(select(.in_reply_to_id == null and (.id as $id | $repliedTo | index($id) == null)))'`
   for genuinely unresolved inline findings: root review comments (`in_reply_to_id ==
   null`) that have *no reply at all yet*. **Do not use `in_reply_to_id == null` by
   itself as "unresolved"** — that only means the comment isn't itself a reply, not
   that nobody has replied to it; once a finding has been fixed and replied to in
   the same round, it is still a root comment forever and would keep being treated
   as a blocker, preventing the loop from ever reaching "no unresolved threads."
   GitHub's review-thread resolution state (`isResolved` via the GraphQL
   `reviewThreads` field) is not a usable substitute either — confirmed empirically
   on a real merged PR that every thread, including ones fixed, replied to, and
   re-reviewed clean by codex, still read `isResolved: false`, because nobody in
   this workflow ever clicks the "Resolve conversation" button; relying on it would
   make every thread look permanently unresolved instead. The
   "has-a-reply-yet" check above is what this skill actually means by "unresolved."
4. `gh api graphql -f query='query($owner: String!, $name: String!, $number: Int!) {
   repository(owner: $owner, name: $name) { pullRequest(number: $number) {
   reviewThreads(first: 100) { nodes { id isResolved comments(first: 1) { nodes {
   databaseId } } } } } } }' -f owner=<owner> -f name=<repo> -F number=<N>` to map
   each root review comment's REST `id` (`databaseId` here) to its GraphQL thread
   node `id`. **`{owner}`/`{repo}` endpoint-path placeholders do not work inside a
   GraphQL query string** — `gh api` only substitutes them in REST endpoint paths
   (confirmed: a literal `"{owner}"` string inside a `-f query=...` GraphQL document
   is sent to GitHub as the literal text `{owner}` and fails to resolve); pass the
   real owner/repo as GraphQL variables via `-f`/`-F` instead, as shown. **This
   query is required before the resolve-thread mutation in "Commit and push" can run
   at all** — `resolveReviewThread`'s `threadId` input is a `PullRequestReviewThread`
   node ID, which only this `reviewThreads` field exposes; the REST `pulls/<N>/comments`
   endpoint used in step 3 above never returns it, and passing a REST comment's
   `node_id` (a `PullRequestReviewComment` ID, a different object type) to the
   mutation fails. Run this once per status check and keep the
   `databaseId → thread id` mapping on hand for every reply posted in this round; with
   more than 100 threads, paginate with `reviewThreads(first: 100, after: $cursor)`.
5. `gh pr view <N> --json mergeable,mergeStateStatus` for merge state.

If the latest top-level comment or inline comment author matches the bot's own GitHub
identity (an echo of a reply or review-trigger comment just posted), take no action —
it is not new external feedback.

### Per-finding sequence

1. Read the full comment body. Do not act on a truncated summary or the badge/title
   alone — findings often have more nuance than the one-line description suggests.
2. **Reproduce before fixing.** Pick the cheapest reliable method:
   - `curl` against a running dev server for REST/API-level findings.
   - A short one-off script using the target framework's local/admin API
     (e.g. with access-control overridden) for data-layer findings.
   - A real browser walkthrough (not a unit test) for UI/flow findings.
   Confirm the bug actually manifests as described before writing any fix. If it does
   not reproduce as described, say so explicitly and investigate why before deciding
   whether the finding is a false positive, narrower, or broader than stated.
3. **Check scope.** Grep for the same pattern (same field, same missing guard, same
   helper) across every other call site in the codebase. If the root cause is broader
   than the finding describes:
   - If it's a small, same-root-cause variant within the current PR's existing diff,
     fix the full scope in this pass.
   - If the broader instance is pre-existing on the target branch (not introduced by
     the current PR) or otherwise substantially out of scope, file it as its own
     tracked issue (per Phase 1, step 5) instead of expanding the current PR, and flag
     it clearly to the human.
4. Apply the fix.
5. **Re-run the exact reproduction from step 2** and confirm it no longer succeeds (for
   an exploit) or now behaves correctly (for a logic bug).
6. **Check regressions**: re-run (or newly run) the legitimate flows that touch the
   same code, to confirm the fix didn't break anything that previously worked.
7. Run the project's full local validation suite.

### Commit and push

- One commit per logical fix, Conventional Commits style.
- Commit body explains the bug, its real-world impact, and exactly how it was verified
  (the reproduction steps and their before/after results) — not just what changed.
- Wrap every identifier, path, and command in backticks in both commit messages and PR
  replies. This is easy to drop under momentum; check it explicitly before posting.
- Push, then reply in-thread (not a new top-level comment) to each finding's original
  comment via the review-comment reply endpoint, citing the fixing commit SHA.
- **Resolve the review thread** for each finding just replied to, using the GraphQL
  `resolveReviewThread` mutation (`gh api graphql -f query='mutation {
  resolveReviewThread(input: {threadId: "<thread-node-id>"}) { thread { isResolved } }
  }'`; get `threadId` from the `reviewThreads` query in status-check step 4 above,
  matched to this finding's comment by `databaseId`). This is
  a separate, easy-to-forget step from posting the reply — the REST reply endpoint has
  no effect on thread resolution, so without explicitly calling this mutation every
  thread stays `isResolved: false` indefinitely, even after being fixed, replied to,
  and re-reviewed clean (confirmed on a real merged PR: every one of 14 fixed,
  replied-to threads still read `isResolved: false`, because this step was never
  performed). Doing this keeps the PR's GitHub UI reflecting reality — reviewers
  scanning the "Files changed" tab see addressed items collapsed rather than a wall of
  comments that all still look open — without changing how this skill itself detects
  "unresolved" (still the has-a-reply-yet check from the status-check step, not
  `isResolved`, since resolving is a deliberate human/agent action that can be skipped
  or delayed, not an automatic consequence of fixing something).
- Trigger a fresh review (e.g. `@codex review`) once all replies are posted and threads
  resolved.

### Loop termination

Repeat the status check → per-finding sequence → commit/push cycle until:

- CI is fully green (or red only for a pre-existing, separately-tracked, out-of-scope
  reason that has been explicitly called out to the human, e.g. via a filed issue from
  Phase 1/4 step 3).
- The latest top-level review comment reports no findings, **and its `Reviewed
  commit` SHA matches the PR's current `headRefOid`** — a clean summary for a
  commit older than the latest push does not satisfy this; re-request review and
  keep looping instead of reporting ready.
- No unresolved inline threads remain.

At that point, report the PR as ready. Do not merge. A prior statement like "merge it
once it's green" is the human's advance intent, not standing authorization to execute
without surfacing the final state for confirmation — name the specific PR and its final
status, and let the human's response (even a short "go ahead") be the actual trigger.

## Watching without polling

- If subscribed to PR webhook activity, react to events; do not poll on a tight
  interval. CI success and new-push events are typically not delivered by webhook —
  use a long fallback check-in (around an hour) to cover that gap, and a short check-in
  (a few minutes) only while actively waiting on an in-progress review pass.
- Never merge any PR without the human naming that specific PR in that turn.
