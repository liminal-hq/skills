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
6. Detect extreme conflict cases: rebase onto `main` succeeds, but merge into integration branch conflicts with current baseline.
7. For extreme conflict cases, set fate to `defer` or `close`, and require `changes-requested` label plus rationale.
8. Ensure label policy prerequisites exist in target repo:
   - create `changes-requested` when missing, description: `Review feedback requested before merge`
   - create `manual-follow-up` when missing, description: `Needs manual attention outside automated integration workflow`
9. For each PR, decide if branch splitting is needed to restore coherent scope.
10. Check commit-message conformance and identify rewrite operations required before merge.
11. Review label correctness and define a label update plan per PR.
12. Explicitly call out any planned force-push operations required by rebase or commit rewrite.
13. Define PR communication plan, including status updates and final fate messaging.
14. Define integration PR title using outcome-first wording with weighted `(#<PR>, #<PR>)` suffix.
15. Score PRs using deterministic model and tie-breakers.
16. Build dry-run commands.
17. Write artefacts:
   - `docs/integration-runs/<date>-<batch>-action-plan.md`
   - `docs/integration-runs/<date>-<batch>-action-plan.json`
   - initialise `docs/integration-runs/<date>-<batch>-checkpoints.json`

## Execute Sequence

1. Require explicit approval of the action plan artefact.
2. Create/switch to integration branch named `integration/<activity-description>`.
3. For each PR, switch to its branch and execute approved split operations when required.
4. Rebase PR branch onto `origin/main` before merge (required for `DIRTY` PRs).
5. If merge against integration branch still conflicts after rebase and PR is in `CHANGES_REQUESTED`, apply approved defer/close path.
5. Rewrite commit messages when required to satisfy Conventional Commit format.
6. Rewrite commit messages when required to satisfy Conventional Commit format.
7. Execute only approved force-push operations after rebase or commit rewrite.
8. Apply approved label updates before merge.
9. Post status comment that PR was automatically processed and is moving to merge.
10. Merge using the required merge commit subject/body format.
11. Post final fate comment (`merged`, `closed`, `deferred`) with rationale.
12. Append checkpoint records after each mutating command.
13. Run validation gates after each step.
14. Finalize on `main` with full validation (`test`, `build`).
15. If opening an integration PR, use approved outcome-first title with `(#<PR>, #<PR>)` suffix so GitHub links references automatically.
16. Write final report artefact.
17. Halt on first failure and trigger rollback policy.

## Label Scope

- This flow does not use `ready` or `blocked` labels for automation decisions.
- Use `manual-follow-up` for leftover PRs that need human attention outside automated processing.

## Tool Packs

## Core Tools

- `gh`: PR listing, metadata, checks, labels, merge operations.
- `git`: branch management, rebase, merge, revert.

## Validation Tools

- `pnpm`, `npm`, or `yarn`: project validation commands.
- `rg`, `jq`: optional triage and artefact processing helpers.
