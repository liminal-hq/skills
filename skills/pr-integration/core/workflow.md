# Workflow

## Modes

1. `audit`: gather PR inventory, score risk, propose merge order, generate run artefacts.
2. `execute`: apply approved plan, run per-step and final validation gates.
3. `resume`: continue from a saved checkpoint artefact.
4. `rollback`: revert the most recent integration step and regenerate plan artefacts.
5. `report`: produce final summary and follow-up items.

## Audit Sequence

1. Confirm preflight (`gh auth status`, `git switch main`, `git pull --ff-only`, clean working tree).
2. List open PRs excluding deferred queue labels.
3. Detect overlapping files, split candidates, and mergeability risk.
4. Classify each PR as `CLEAN`, `DIRTY`, or `BLOCKED`.
5. For each `DIRTY` PR, add rebase-on-`origin/main` before-merge commands to the plan.
6. For each PR, decide if branch splitting is needed to restore coherent scope.
7. Check commit-message conformance and identify rewrite operations required before merge.
8. Explicitly call out any planned force-push operations required by rebase or commit rewrite.
9. Score PRs using deterministic model and tie-breakers.
10. Build dry-run commands.
11. Write artefacts:
   - `docs/integration-runs/<date>-<batch>-action-plan.md`
   - `docs/integration-runs/<date>-<batch>-action-plan.json`
   - initialise `docs/integration-runs/<date>-<batch>-checkpoints.json`

## Execute Sequence

1. Require explicit approval of the action plan artefact.
2. Create/switch to integration branch.
3. For each PR, switch to its branch and execute approved split operations when required.
4. Rebase PR branch onto `origin/main` before merge (required for `DIRTY` PRs).
5. Rewrite commit messages when required to satisfy Conventional Commit format.
6. Execute only approved force-push operations after rebase or commit rewrite.
7. Merge using the required merge commit subject/body format.
8. Append checkpoint records after each mutating command.
9. Run validation gates after each step.
10. Finalize on `main` with full validation (`test`, `build`).
11. Write final report artefact.
12. Halt on first failure and trigger rollback policy.

## Tool Packs

## Core Tools

- `gh`: PR listing, metadata, checks, labels, merge operations.
- `git`: branch management, rebase, merge, revert.

## Validation Tools

- `pnpm`, `npm`, or `yarn`: project validation commands.
- `rg`, `jq`: optional triage and artefact processing helpers.
