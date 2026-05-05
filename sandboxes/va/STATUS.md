# STATUS — va

Last updated: 2026-05-05

> One-glance status for the handoff-team sandbox. Read this first when the operator lands here for a small follow-up. Only load CLAUDE.md / CONTEXT.md / brief files if the task isn't already mapped here.
> Update at end of any session that ships a build pack, fields a question from the handoff team, or shifts a thread. Keep under 60 lines.

---

## Active threads

> One line each. Active build packs, open punch-list rounds, VA questions awaiting orchestrator response.

## Next moves

> Top 3, in execution order.

## Blocked on operator

> What's waiting on a human decision — final asset, copy approval, scope confirmation.

## Recently shipped (last 7 days)

> Dated bullets. Build packs handed to the VA, punch lists sent, deliveries confirmed.

## Reminders specific to this sandbox

- No-edit-after-handoff is the hard rule (CLAUDE.md). Update via punch-list, never via direct edit of the original spec
- Every build pack file should be added to `handoff-files-guard.py` `HANDOFF_MARKERS` once handed off — the hook will prompt before any future edit lands
- Per-deliverable tracker updates only after the VA confirms delivery, not when the pack is shipped
