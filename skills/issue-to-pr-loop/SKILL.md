---
name: issue-to-pr-loop
description: Drive a tracked issue from investigation through a merge-ready pull request — research and surface real decisions before implementing, verify each piece as it's built, spin off out-of-scope discoveries as new issues, then run repeated rounds of automated review until clean, reproducing every finding before fixing it.
---

# Issue to PR Loop

Use these canonical documents:

- `./core/intent.md`
- `./core/workflow.md`
- `./core/guardrails.md`

## Notes

- Use `gh` for issue/PR creation, status, and review-comment operations.
- Use `git` for branch and commit operations.
- Require explicit, per-PR approval before merging — a prior "merge once green"
  statement is advance intent, not standing authorization.
- Spin off out-of-scope discoveries as new tracked issues rather than expanding the
  current PR.
- See `./references/reply-template.md` for the in-thread review-reply format.
