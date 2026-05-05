# _ARCHIVE-MONTH.md — Monthly archive sweep

> Operator-triggered routine. Once a month, sweep posted items from the prior month into the **out-of-tree archive folder** (configured per-operator — typically `~/Desktop/<project>-Archive/` or similar) so active sandboxes stay token-light. Briefs and drafts move; rendered outputs (PNGs, PDFs) stay where they are.

**Architecture:** Archive lives OUTSIDE the project folder, at a sibling location like `~/Desktop/<project>-Archive/YYYY-MM/<sandbox-name>/<original-subpath>/`. Workers and orchestrator NEVER scan, list, or read from the Archive folder during normal operations — it's accessed only by explicit operator dispatch. This is what saves tokens session-over-session: archived files don't appear in any `ls`, `find`, or `grep` from inside the project folder.

---

## Cadence

Once a month. Suggested: **first weekly maintenance pass of the new month** (e.g., the first Sunday of June archives May items). Operator-triggered, never auto-fires.

Trigger phrases: *"archive [month]"* (e.g., "archive May") · *"monthly archive"* · *"sweep posted"*

---

## What gets archived vs. stays

**ARCHIVE (move to `<external archive>/YYYY-MM/<sandbox>/<subpath>/`):**
- Briefs: `*-brief.md`, `*-design-brief.md`, `*-cover-brief.md`, `*-design-brief-Concept-A.md` etc., once their referenced output is shipped + post date is in the prior month
- Drafts: `*-draft.md` once the final has shipped
- Source MDs: `*-post.md`, `*-script.md`, `*-captions.md` once posted
- Per-piece copy files (e.g., article markdown source) once the article is posted

**STAYS (do not move):**
- Rendered outputs: PNGs, PDFs, JPGs in `final/`, `slides/`, `thumbnails/`, etc. — these may be re-shared, referenced, or used as templates for future work
- Anything with status NOT "Posted" in the per-deliverable tracker (Ready, Partial, In Progress, Draft)
- Files explicitly flagged "evergreen — do not archive" by the operator
- Cross-referenced briefs: a brief still cited by an active calendar entry, future scheduled post, sibling brief, or sandbox `CLAUDE.md` / `CONTEXT.md`
- Reference docs in `_config/`, brand intelligence, books-in-progress

---

## Folder convention

Archive lives **outside** the project folder. Each archive run creates a `YYYY-MM/` subfolder, then mirrors the original sandbox path inside it so any file can be located by its original location.

```
<external archive root>/
└── 2026-05/
    ├── content-claude/
    │   ├── articles/
    │   ├── podcast/briefs/
    │   ├── posts/
    │   └── chapter-optins/
    ├── design-claude/
    │   ├── articles/briefs/
    │   ├── instagram/
    │   └── Book Cover/[Title]/
    └── briefs/        ← root-level briefs that archived this month
```

The project folder itself stays clean — no `_archive-*/` subfolders inside any sandbox or at the root. Workers and orchestrator only scan active surfaces.

**Why outside-tree:** archived files inside the sandbox still cost tokens on every `ls`, `find`, `grep`, and on every session that references those folders. Outside-tree means zero scan cost, zero session cost.

---

## Routine (orchestrator runs in this order)

### Phase 1 — Identify candidates

Read the per-deliverable tracker. Build a candidate list. For every row marked "Posted [date]" where [date] falls in the target month:

- Source file path (the brief / draft / copy MD that produced it)
- Rendered output path (this STAYS — log it for reference, do not move)
- Cross-reference check: grep the source filename across `CLAUDE.md`, `CONTEXT.md`, all sandbox `CLAUDE.md`s, all live briefs in `briefs/`, the active calendar(s). Note any references found.

Also scan briefs/ for `YYYY-MM-*.md` briefs whose Acceptance criteria all check out — they are archive-eligible even if not directly tracked.

### Phase 2 — Operator validation gate

Surface the candidate list to the operator before moving anything. Format:

| Item | Source file | Rendered output (stays) | Cross-refs | Move? |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | y / n / evergreen |

Operator approves, edits, or excludes individual items. Operator can tag any item as "evergreen — do not archive" and that flag persists for future archive runs (record in `_log/ARCHIVE-LOG.md`).

### Phase 3 — Move + update

For each operator-approved item:

1. Create the destination archive subfolder if it doesn't exist: `<external archive>/YYYY-MM/<sandbox>/<original-subpath>/` (mirror source structure exactly)
2. Move the source file using `mv` (preserve filename — do not rename, do not add suffixes)
3. Update the per-deliverable tracker row: change status from "Posted [date]" to "Archived YYYY-MM" — but **do not rewrite the path column to the archive path**. The path column stays as the original sandbox path so future grep-by-path still finds the row's history.
4. Search-and-clear stale references: grep the old path across `CLAUDE.md`, `CONTEXT.md`, sandbox `CLAUDE.md`s, other briefs. For each hit: if the reference is load-bearing (active dependency), the file shouldn't have been archived — restore. If the reference is a stale historical mention, remove the line or update to reference the archive path explicitly.

**Delete-on-encounter rule:** during any phase of this routine, if a duplicate file is encountered (same filename + same content in two locations), delete the duplicate instead of archiving twice. Note in the change log.

### Phase 4 — Verify

- [ ] Every operator-approved item moved
- [ ] Every relevant per-deliverable tracker row updated to "Archived YYYY-MM"
- [ ] No broken links: grep for any old path, confirm no hits remain (or all hits now point to the archive path)
- [ ] One-line summary appended to `_log/ARCHIVE-LOG.md`: *"YYYY-MM-DD · archived YYYY-MM · N items across X sandboxes · M items flagged evergreen and skipped"*
- [ ] No rendered output (PNG/PDF) was moved by accident

---

## Status legend (for the per-deliverable tracker)

The "HOW TO USE" section gets one new status:

- **Ready** = fully produced, not yet posted
- **Posted** = live on platform, with date
- **Partial** = written but design not complete, or vice versa
- **Archived** = posted + source files moved to external archive

---

## Anti-patterns (don't do these)

- **Don't archive items that haven't been posted.** Archive ≠ "I'm done with it." Archive = "shipped + month closed." Use `briefs/done/` for completed-but-non-shipped work.
- **Don't archive rendered outputs.** PNGs and PDFs stay in active folders — they may get re-shared, re-used, or referenced. The brief that produced them is what generates clutter, not the asset.
- **Don't archive cross-referenced briefs.** If a calendar entry, another brief, or an active series still references it, leave it alone until the dependency clears.
- **Don't auto-archive without operator validation.** The operator has context the orchestrator doesn't ("I want to re-render that one for a re-share next week").
- **Don't run mid-month.** The boundary is monthly; archiving partial months creates fragmentation.
- **Don't rename files when moving.** Preserve the filename so any sleeping cross-reference can be found and updated, not silently broken.
- **Don't combine the archive routine with weekly maintenance in the same pass.** Both are sweeps; mixing them creates context drift.

---

## Inputs

| Layer | File | Why |
| --- | --- | --- |
| 4 | per-deliverable tracker | source of truth for posted status + file paths |
| 4 | `briefs/YYYY-MM-*.md` (target month) | candidate root-level briefs |
| 4 | sandbox folders | grep target for cross-references |
| 4 | `_log/ARCHIVE-LOG.md` (creates if absent) | persistent record + evergreen flags |

---

## Returns

- Updated per-deliverable tracker (rows reflect "Archived YYYY-MM" status)
- New `YYYY-MM/` folder populated in the external archive
- Updated cross-references in any file that pointed to the old path
- One-line entry appended to `_log/ARCHIVE-LOG.md`
- Operator-validated change log: "this archive pass moved N items from [month], flagged X as evergreen, skipped Y because still cross-referenced"
