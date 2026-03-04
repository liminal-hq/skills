# PR Integration (Aider)

Follow the canonical workflow and guardrails:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Aider Adapter Notes

- Run `audit` before any mutating step.
- Require explicit approval before `execute`.
- Keep git mutation commands sequential (`switch`, `rebase`, `merge`, `revert`).
- Log mutating command provenance in checkpoint artefacts.
- Do not push unless explicitly requested.
