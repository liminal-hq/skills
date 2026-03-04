# PR Integration (Gemini CLI)

Use the core documents as canonical:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Gemini CLI Adapter Notes

- Execute in two phases: `audit` then approved `execute`.
- Use `gh` and `git` as primary orchestration tools.
- Record checkpoint entries after each mutating command.
- Rebase `DIRTY` PR branches onto `origin/main` before merge attempts.
- Do not push unless explicitly requested.
