# _IDEAS-PROCESSING.md — Orchestrator routine for the ideas inbox

> Run when the operator says *"process ideas"*. Routes tagged bullets from `ideas.md` to their destination files; leaves untagged bullets alone.

---

## When to run

Trigger phrases: *"process ideas"*, *"route ideas"*, *"clear inbox"*, or any equivalent.

Also: surface count of pending tagged bullets at the start of weekly maintenance (Phase 2 of `_WEEKLY-MAINTENANCE.md`).

---

## Routine

1. **Read `ideas.md`** at project root.
2. **Identify tagged bullets** — any bullet containing `#tag` (see tag table in `ideas.md`).
3. **For each tagged bullet:**
   - Look up destination file in the tag table.
   - Confirm destination file exists. If it doesn't, surface in the report (don't create it silently).
   - Append the bullet to the destination file (verbatim, minus the tag).
   - Mark the bullet in `ideas.md` as routed (move to a `## Routed` section at the bottom with date) — do NOT delete; the audit trail is cheap.
4. **Voice / token tags (`#voice`, `#token`)** require operator confirmation before applying. Surface as proposals in the report. Do not auto-write to `_config/BRAND.md` or `_config/REFERENCE.md`.
5. **Leave untagged bullets in place.** Don't guess where they belong.
6. **Report back** to the operator:
   - Routed: N bullets → list of destinations
   - Pending operator review: voice/token proposals (full text)
   - Unrouted (untagged): N bullets remaining in inbox
   - Missing destination files (if any): list

---

## Rules

- **Append, don't restructure.** Destination files have their own structure — your job is to add the bullet to an appropriate ideas/notes section, not to reorganize the file.
- **Preserve the tag in the routed-archive section** so the audit trail tells you *why* a bullet was routed there. Strip the tag from the destination file copy.
- **Don't auto-create destination files.** If the path doesn't exist, surface it. Operator decides whether to create.
- **Multiple tags on one bullet** = route to all destinations, archive once. Note all destinations in the routed archive.
- **Untagged stays untagged.** Don't infer tags from content.

---

## Routed archive format (in `ideas.md`)

```markdown
## Routed

| Date | Bullet (verbatim with original tags) | Destination(s) |
| --- | --- | --- |
| 2026-05-03 | revisit the [topic] cue for [format] #content | content-claude/ideas-inbox.md |
```

Keep the archive table short — when it exceeds 50 rows, move oldest 30 to `_log/ideas-archive.md` (create if it doesn't exist).

---

## Tag table (canonical)

Defined in `ideas.md`. If a new tag pattern emerges (used 3+ times by operator), surface as a proposal to add it to the canonical table. Don't expand the table without operator approval.
