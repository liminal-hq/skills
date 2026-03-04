# PR Integration (Claude)

Follow these canonical documents:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Claude Adapter Notes

- Use deterministic ordering for merge sequencing.
- Require explicit approval between `audit` and `execute`.
- Keep git mutation operations sequential and logged.
- Write run artefacts using `../../references/action-plan-template.md`.
