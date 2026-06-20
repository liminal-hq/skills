# Issue to PR Loop (Codex)

Follow these canonical documents:

- `../../core/intent.md`
- `../../core/workflow.md`
- `../../core/guardrails.md`

## Codex Adapter Notes

- Use `gh` for status, comment, and reply operations exactly as in `core/workflow.md`.
- Since this skill drives codex review on a PR, be explicit in your own commentary
  about which actions are yours versus the reviewing codex bot's — do not conflate the
  acting agent with the review bot when summarizing status back to the human.
- Treat a PR's own `@codex review` trigger as an external dependency with its own
  latency; do not assume a review pass has completed just because the trigger comment
  was posted successfully.
