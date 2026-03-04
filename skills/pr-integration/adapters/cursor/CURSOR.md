# PR Integration (Cursor)

Use these files as the single source of behaviour:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Cursor Adapter Notes

- Build an action plan artefact in `audit` mode.
- Pause for explicit human approval between `audit` and `execute`.
- Run validation gates after each integration step.
- Stop immediately on failure and trigger rollback workflow.
- Keep internal triage details out of outward PR content.
