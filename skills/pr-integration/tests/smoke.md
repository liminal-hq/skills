# Smoke Tests

## Scenario 1: Clean audit

- Preconditions: clean `main`, authenticated `gh`, at least two open PRs.
- Expectation: action plan markdown/JSON artefacts and initial checkpoint artefact are generated.

## Scenario 2: Failed validation during execute

- Preconditions: selected PR fails test or build gate.
- Expectation: execution halts, rollback runs, artefacts are regenerated.

## Scenario 3: Dirty PR branch

- Preconditions: one PR reports merge state `DIRTY`.
- Expectation: rebase onto `origin/main` occurs before merge attempt.

## Scenario 4: Resume from checkpoint

- Preconditions: interrupted execution with non-empty checkpoints artefact.
- Expectation: `resume` continues from the first incomplete step and preserves prior records.

## Scenario 5: Split and commit rewrite planning

- Preconditions: one PR has overlap requiring split and non-conforming commit messages.
- Expectation: `audit` artefact includes split plan, rewrite plan, and explicit force-push approval requirement before `execute`.

## Scenario 6: Label review and update planning

- Preconditions: one PR is missing required labels and one has stale labels.
- Expectation: `audit` artefact includes label review findings and approved label update plan before merge.

## Scenario 7: Fate messaging coverage

- Preconditions: one PR merges, one PR is deferred, and one PR is closed due to split fallout.
- Expectation: each PR receives processing comment plus final fate comment with rationale and next steps.

## Scenario 8: Integration branch naming

- Preconditions: planned branch name does not describe activity (for example `integration/2026-03-04-batch-01`).
- Expectation: audit marks branch naming check as failed and requires `integration/<activity-description>` before execute.

## Scenario 9: Integration PR title ordering

- Preconditions: planned title is process-prefixed (for example `Batch 01 integration: ...`).
- Expectation: audit fails title policy check and rewrites to outcome-first title with `(#<PR>, #<PR>)` suffix.

## Scenario 10: PR reference link formatting

- Preconditions: planned integration PR title lists provenance without GitHub references (for example `(12, 14)`).
- Expectation: audit fails reference-link check and rewrites suffix to `(#12, #14)`.

## Scenario 11: Rebase-clean but integration-conflict with changes requested

- Preconditions: PR rebases onto `main`, but conflicts against integration branch baseline and review state remains `CHANGES_REQUESTED`.
- Expectation: audit plans `defer` or `close`, ensures `changes-requested` label exists (description: `Review feedback requested before merge`), and posts final fate rationale with follow-up recommendation.

## Scenario 12: Leftover manual-follow-up labelling

- Preconditions: PR is intentionally left outside automated processing for later human work.
- Expectation: `manual-follow-up` label exists (description: `Needs manual attention outside automated integration workflow`) and PR receives next-step guidance comment.
