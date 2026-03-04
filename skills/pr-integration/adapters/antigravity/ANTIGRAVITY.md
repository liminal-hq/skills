# PR Integration (Antigravity)

Follow these canonical documents:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Antigravity Adapter Notes

- Run in two phases: `audit` first, then `execute` only after explicit approval.
- Keep critical git operations sequential (`switch`, `rebase`, `merge`, `revert`).
- Record mutating command provenance in checkpoint artefacts.
- Use deterministic PR scoring and tie-breakers from core workflow.
- Do not push remote changes unless the user explicitly requests push.

## Expected Tools

- `gh` for PR inventory, labels, checks, and merge metadata.
- `git` for branch orchestration and rollback.
- `pnpm`, `npm`, or `yarn` for validation commands.

## Required Artefacts

- `docs/integration-runs/<date>-<batch>-action-plan.md`
- `docs/integration-runs/<date>-<batch>-action-plan.json`
- `docs/integration-runs/<date>-<batch>-checkpoints.json`
- `docs/integration-runs/<date>-<batch>-final-report.md`
