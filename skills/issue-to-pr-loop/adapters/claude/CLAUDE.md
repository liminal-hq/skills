# Issue to PR Loop (Claude)

Follow these canonical documents:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Claude Adapter Notes

- Use the `AskUserQuestion` tool (or equivalent structured-choice primitive) when
  Phase 1 surfaces a genuine architectural decision — present concrete options with a
  recommendation rather than asking an open-ended question.
- Use `gh issue create` for spinning off out-of-scope discoveries; check
  `gh label list`/`gh issue list --search` first so the new issue uses existing labels
  and doesn't duplicate something already tracked.
- Use `gh api repos/{owner}/{repo}/pulls/<N>/comments/<id>/replies` for in-thread
  review replies, not `gh pr comment`, which posts a new top-level comment instead of
  a threaded reply. `gh api` only substitutes the literal `{owner}`/`{repo}`/`{branch}`
  placeholders in REST endpoint paths — not Octokit-style `:owner`/`:repo`.
- Use the `ScheduleWakeup` tool (or equivalent scheduling primitive) for the fallback
  check-in cadence described in `../../core/workflow.md` — short (3-5 min) while
  actively waiting on a review pass in the current turn, long (~1 hour) as the webhook
  gap-filling fallback.
- When asked to "watch" or subscribed to PR webhook activity, react to delivered
  events rather than polling; re-arm the long fallback check-in after each event that
  doesn't fully resolve the loop.
- For empirical reproduction, prefer the target project's local/admin API with access
  control explicitly overridden (e.g. Payload's `overrideAccess: true`) over crafting
  raw HTTP requests when both are available — it is faster to script and easier to
  clean up afterward.
- Confirm the Skill tool is loaded for this skill before relying on it; if it has not
  been installed into the active project's skill set, fall back to following
  `core/workflow.md` directly without the slash-invocable wrapper.
