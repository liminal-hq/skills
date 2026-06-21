# In-thread reply template

Use this shape when replying to a codex finding via the review-comment reply endpoint.

```
Confirmed and fixed in <short-sha>. <One sentence on the root cause, in backticks where
code is named.> <One sentence on the fix.> Verified <directly|via Playwright|via curl>:
<what you did> confirmed <before-state>; after the fix, <after-state>.
```

## Rules

- Cite the actual fixing commit's short SHA, not "see the latest commit."
- State what was true *before* the fix and what's true *after* — both halves, not just
  the after-state. This is what makes the reply verifiable evidence rather than a
  restatement of intent.
- If the finding turned out to be broader than stated (same root cause on other
  fields/call sites), say so explicitly and name what else was fixed in the same pass.
- If you were wrong about something in an earlier reply or an earlier session decision
  (e.g. "I thought X wasn't checked, but it turns out Y hook does check it"), say so
  plainly rather than glossing over the correction.
- Wrap every identifier, path, and command in backticks. Re-read the rendered comment
  body before posting if there is any doubt.

## Example (drawn from a real review round)

> Confirmed and fixed in `004ffc3` — fully reproduced your exact exploit before
> fixing. Created an account for a victim's email with an attacker-chosen password,
> logged in as an unrelated already-verified member, read the victim's
> `email_verify` notification row via `GET /api/notifications`, pulled the live
> `emailVerifyToken` out of `templateVars`, redeemed it at `/api/verify-email`, then
> logged in as the victim with the attacker-chosen password — confirmed it worked
> exactly as described before the fix. Restricted `read`/`create`/`update`/`delete`
> on `Notifications` to staff. Re-ran the exploit after the fix (now 403s for a
> regular member) and confirmed staff can still read the row.
