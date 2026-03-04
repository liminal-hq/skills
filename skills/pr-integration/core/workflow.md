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
3. Score PRs using deterministic model and tie-breakers.
4. Detect overlapping files and mergeability risk.
5. Build dry-run commands.
6. Write artefacts:
   - `docs/integration-runs/<date>-<batch>-action-plan.md`
   - `docs/integration-runs/<date>-<batch>-action-plan.json`
   - initialise `docs/integration-runs/<date>-<batch>-checkpoints.json`

## Execute Sequence

1. Require explicit approval of the action plan artefact.
2. Create/switch to integration branch.
3. For `DIRTY` PRs, rebase onto `origin/main` before merge.
4. Integrate PRs in approved order.
5. Append checkpoint records after each mutating command.
6. Run validation gates after each step.
7. Finalize on `main` with full validation (`test`, `build`).
8. Write final report artefact.
9. Halt on first failure and trigger rollback policy.

## Tool Packs

## Core Tools

- `gh`: PR listing, metadata, checks, labels, merge operations.
- `git`: branch management, rebase, merge, revert.

## Validation Tools

- `pnpm`, `npm`, or `yarn`: project validation commands.
- `rg`, `jq`: optional triage and artefact processing helpers.
