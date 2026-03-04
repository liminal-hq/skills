# Skills Architecture

## Model

Each skill follows a core-plus-adapter model:

- `core/` defines behaviour, ordering, and safety policy.
- `adapters/<agent>/` maps core behaviour to agent-specific instruction format.

## Versioning

- Each skill has independent semantic versioning in `skill.yaml`.
- Behaviour changes require version bumps.

## Safety

- Mutating operations must be logged in run artefacts.
- Execution must stop on failed validation gates.
- Rollback steps must be documented per skill.
