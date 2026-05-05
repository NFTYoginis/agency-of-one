# STATUS — content-claude

Last updated: 2026-05-05

> One-glance status for the content sandbox. Read this first when the operator (or orchestrator dispatch) lands here for a small follow-up. Only load CLAUDE.md / CONTEXT.md / brief files if the task isn't already mapped here.
> Update at end of any session that ships a draft, dispatches a brief, or shifts a thread. Keep under 60 lines.

---

## Active threads

> One line each. What's open right now in the content sandbox.

## Next moves

> Top 3, in execution order.

## Blocked on operator

> What's waiting on a human decision (next article topic, draft approval, etc.).

## Recently shipped (last 7 days)

> Dated bullets. Older entries graduate out.

## Reminders specific to this sandbox

- Source MD moved to `posts/done/` only after operator confirms post is live (per CLAUDE.md)
- All prose deliverables must run `/humanizer` before moving to `final/` (per `../_config/_WORKER-RULES.md` § 7)
- Never write to root per-deliverable tracker from a draft state — orchestrator updates only after operator confirmation
