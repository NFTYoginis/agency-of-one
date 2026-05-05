# _MONTHLY-MAINTENANCE.md — The monthly architecture sweep

> Runs on the first Sunday of each calendar month, immediately after weekly maintenance. Handles the heavier structural compression that's too expensive to do every week — archive moves, deeper `_config/` audit, MEMORY.md / root CLAUDE.md condensing, calendar build for the next month, monthly audit log update.

---

## Cadence

Once a month, on the **first Sunday** of the calendar month, after weekly maintenance completes in the same session (or a fresh session immediately after).

Trigger phrase: *"monthly maintenance"*, *"monthly sweep"*, *"monthly audit"*.

The weekly maintenance routine surfaces this as the next thing to run if the date qualifies — but the operator dispatches it explicitly. Don't auto-run inside the weekly session.

---

## Roles

Same as weekly maintenance:

| Actor | What they do |
| --- | --- |
| **Workers** | Already purged in the weekly that just ran. Not dispatched again here. |
| **Orchestrator** | Heavier structural compression; auto-triggers `archive [month]`; updates monthly audit log; condenses always-loaded surface |
| **Operator** | Validates structural changes (especially archive moves and root CLAUDE.md condensing); confirms calendar build for upcoming month |

---

## Routine (orchestrator runs in this order)

### Phase 1 — Auto-trigger `archive [month]` for prior month

Run the `briefs/_ARCHIVE-MONTH.md` routine on the **prior** calendar month (e.g. on first Sunday of June, archive May). Source files for posted prior-month items move OUT of the project folder entirely, into the configured external archive location. Rendered outputs (PNGs, PDFs) stay in their active folders. Operator validates each move per the existing archive-month spec.

This is the biggest scan-surface compression of the month — keeps the project folder bounded to current-month work, and archived files cost zero tokens during normal sessions because they're outside the project tree entirely.

**Apply the delete-on-encounter rule:** during this phase, any duplicate file encountered (same filename + same content in two locations) gets deleted, not archived twice. Note in the change log.

### Phase 2 — Monthly audit log update

Read `briefs/_MONTHLY-AUDIT-LOG.md`. Run the checkmark pass for the architectural additions (ideas inbox, energy-matched briefs, retrospectives, hooks, exemplar tables, hashtag rules, etc.). For each:

- Confirm whether it's still being used
- Decide: keep, adapt, or retire
- Update the log with a new month row
- Surface retire/adapt candidates to the operator for decision

This is the one-mechanism check that prevents architectural cruft from accumulating silently.

### Phase 3 — Always-loaded surface compression

For each file flagged in last weekly maintenance's Phase 2 step 10 (token-surface measurement) as growing or approaching caps:

- **`MEMORY.md` index** — if approaching 180 lines, identify entries to archive (move to `_archive/` subfolder inside the memory folder), merge overlapping entries, or split the index into scoped files. Surface candidates; operator decides.
- **Root `CLAUDE.md`** — identify sections that have grown and propose moves to route-discoverable locations (`_config/`, a sandbox CLAUDE.md, a brief template). Don't apply — surface as a proposal.
- **Sandbox `CLAUDE.md` / `CONTEXT.md`** — same: identify sections that could move to `_config/_WORKER-RULES.md` (cross-cutting), to a brief template (per-task), or to a route-discoverable file inside the sandbox.

Goal: keep always-loaded surface bounded so per-session token cost doesn't grow with the project.

### Phase 4 — Deeper `_config/` audit

Read `BRAND.md`, `REFERENCE.md`, `RELATED_PROJECTS.md`, `_WORKER-RULES.md`, `COMMON-MISTAKES.md` in full. Look for:

- Stale rules (was true at the time, no longer applies)
- Duplicated rules across files (collapse to single source of truth)
- New patterns from the past month's work that should be codified here but aren't yet
- Sections too long to scan quickly (candidates for further splitting)

Propose changes; operator validates before applying. Don't restructure speculatively.

### Phase 5 — Cross-sandbox registry consistency

Verify these all agree with each other and with reality on disk:

- Root `CLAUDE.md` `## SANDBOXES` table
- Root `CONTEXT.md` task-routing rows
- `MEMORY.md` Scopes table
- `_config/RELATED_PROJECTS.md` for off-folder projects

Any sandbox missing from any registry → flag. Any registry entry pointing at a folder that no longer exists → flag.

### Phase 6 — Next month's calendar build

If a calendar for the upcoming month doesn't exist yet, run the `build [month] calendar` routine (`briefs/_CALENDAR-TEMPLATE.md`). Don't pre-emptively build for two months out — that's calendar-creep and the angles get stale.

### Phase 7 — Operator validation gate

Same shape as weekly Phase 3 — present proposed changes as a summary, operator approves/edits/rejects each, orchestrator applies approved changes, rejections logged.

---

## Deliverables (what monthly maintenance produces)

- Prior-month source files archived (via `archive [month]` routine)
- Monthly audit log row added; retire/adapt decisions logged
- Always-loaded surface compressed (memory + root CLAUDE.md + sandbox CLAUDE.mds bounded)
- `_config/` audit deltas applied
- Registry consistency restored
- Next month's calendar exists (or confirmed not-yet-needed)
- Operator-validated change log: one paragraph: "this month we archived X, condensed Y, retired Z"

---

## Anti-patterns

- **Don't run monthly maintenance on a non-first-Sunday.** Cadence matters; off-cadence runs make the audit log non-comparable across months.
- **Don't compress always-loaded files speculatively.** Only compress what's been flagged by weekly's measurement phase as actually growing.
- **Don't auto-apply `_config/` changes.** Brand voice, banned vocabulary, key phrases — the operator owns these calls.
- **Don't pre-emptively archive current-month source files.** Active month stays active. Only the prior month gets archived.
- **Don't extend the routine to include unrelated projects.** Monthly maintenance is for this orchestrator's house, not for related properties — those have their own maintenance cadences if they need them.

---

## Inputs (Layer 3 / Layer 4)

| Layer | File | Why |
| --- | --- | --- |
| 3 | `_config/BRAND.md`, `REFERENCE.md`, `RELATED_PROJECTS.md`, `_WORKER-RULES.md`, `COMMON-MISTAKES.md` | Phase 4 deeper audit |
| 4 | `MEMORY.md` (user memory) | Phase 3 compression candidates |
| 4 | `briefs/_MONTHLY-AUDIT-LOG.md` | Phase 2 log update |
| 4 | Root `CLAUDE.md`, sandbox `CLAUDE.md` / `CONTEXT.md` | Phase 3 + Phase 5 audits |
| 4 | Last weekly maintenance's measurement output | Phase 3 input — what to compress |

---

## Verify (orchestrator runs before declaring monthly maintenance complete)

- [ ] Prior-month archive run + operator-validated
- [ ] Monthly audit log has a new row for this month
- [ ] All flagged always-loaded files have been compressed or explicitly deferred with a reason
- [ ] `_config/` audit deltas applied or deferred
- [ ] All registries (root CLAUDE.md, root CONTEXT.md, MEMORY scopes, RELATED_PROJECTS) agree with reality on disk
- [ ] Next month's calendar exists or has a deferred-with-reason note
- [ ] One-paragraph change log written and shown to operator

---

## Estimated time

~60 minutes if nothing requires deep restructuring. ~2 hours if Phase 3 surfaces a real always-loaded compression opportunity (e.g. splitting MEMORY.md or refactoring a bloated sandbox CLAUDE.md). The variance is acceptable — monthly is the right cadence for that kind of work.
