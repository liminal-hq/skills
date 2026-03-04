---
name: pr-integration
description: Review and integrate pull requests with audit and execute flows, conflict-aware ordering, validation gates, checkpointing, and rollback safeguards.
---

# PR Integration

Use these canonical documents:

- `./core/intent.md`
- `./core/workflow.md`
- `./core/guardrails.md`

## Codex Notes

- Use `gh` for PR inventory, labels, checks, and merge metadata.
- Use `git` for branch orchestration and rollback operations.
- Generate run artefacts from `./references/action-plan-template.md`.
- Require explicit approval between `audit` and `execute`.
- Do not push unless explicitly asked.
