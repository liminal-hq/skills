# Guardrails

## Required Gates

1. Preflight passes.
2. Review standards pass (scope coherence, regressions, security, docs impact).
3. Validation commands pass for each integration step and at batch end.
4. Commit-message conformance is verified, with rewrite plan approved when needed.
5. Any force-push operations are predeclared in `audit` and explicitly approved.

## Safety Rules

- Never merge directly from local `main` unless explicitly requested.
- Run critical git operations sequentially:
  - `git switch`
  - `git merge`
  - `git rebase`
  - `git cherry-pick`
- Stop immediately on failed gate.
- Keep internal triage details out of outward PR content.
- Preserve literal backticks in merge/commit messages and PR text.
- Use file-based message input when shell commands include backticks.

## Rollback

If a gate fails:

1. Stop execution.
2. Revert the most recent integration commit.
3. Re-run validation.
4. Regenerate action plan artefacts from current state.
