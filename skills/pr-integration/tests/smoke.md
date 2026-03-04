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
