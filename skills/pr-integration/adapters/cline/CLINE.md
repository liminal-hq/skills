# PR Integration (Cline)

Apply canonical behaviour from:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Cline Adapter Notes

- Use deterministic scoring and tie-breakers from core workflow.
- Execute branch operations sequentially; do not parallelize mutating git commands.
- Persist run artefacts (`action-plan`, `checkpoints`, `final-report`) for each batch.
- Treat rollback as mandatory on failed gates.
- Do not push remote updates without explicit user request.
