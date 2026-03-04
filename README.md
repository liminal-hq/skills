# liminal-hq/skills

Shared, multi-agent skills for Liminal HQ workflows.

## Goals

- Keep skill logic agent-agnostic and reusable.
- Keep agent-specific instructions thin and explicit.
- Ship versioned, testable skills with clear guardrails.

## Repository Layout

- `skills/<name>/core/`: canonical intent, workflow, and guardrails.
- `skills/<name>/adapters/<agent>/`: adapter entrypoint for each agent.
- `skills/<name>/references/`: templates and supporting documents.
- `skills/<name>/tests/`: scenario and regression tests for skill behaviour.
- `schemas/`: metadata schema definitions.
- `scripts/`: validation and maintenance scripts.

## Install (Codex)

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo liminal-hq/skills \
  --path skills/pr-integration/adapters/codex \
  --name pr-integration
```

## Conventions

- `core/` is the source of truth.
- Adapters must preserve core behaviour and safety gates.
- Skill metadata lives in `skill.yaml` and must validate against `schemas/skill.schema.json`.
