# Guardrails

## Required Gates

1. Preflight passes.
2. Review standards pass (scope coherence, regressions, security, docs impact).
3. Validation commands pass for each integration step and at batch end.
4. Commit-message conformance is verified, with rewrite plan approved when needed.
5. Any force-push operations are predeclared in `audit` and explicitly approved.
6. Label policy review passes, and required label updates are planned before `execute`.
7. PR communication plan is approved, including automated status and final fate comments.
8. Integration branch name follows `integration/<activity-description>`, not date-only or batch-only names.
9. Integration PR title is outcome-first and includes weighted provenance suffix using GitHub-linkable references (`#<PR>`).
10. `changes-requested` label exists in target repo; create it during `audit` when missing with description `Review feedback requested before merge`.
11. `manual-follow-up` label exists in target repo; create it during `audit` when missing with description `Needs manual attention outside automated integration workflow`.

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
- Ensure each processed PR receives a clear final fate message (`merged`, `closed`, or `deferred`) with concise rationale.
- Do not prefix integration PR titles with process-only terms such as `Batch`, `Round`, or `Wave`.
- When listing PR provenance, always use `#<PR>` references so GitHub autolinks related PRs.
- If rebase succeeds but integration-branch merge still conflicts and review state is `CHANGES_REQUESTED`, do not force merge; mark fate as `deferred` or `closed` with rationale.
- For leftover PRs outside automated handling, apply `manual-follow-up` label and include next-step guidance.

## Rollback

If a gate fails:

1. Stop execution.
2. Revert the most recent integration commit.
3. Re-run validation.
4. Regenerate action plan artefacts from current state.
