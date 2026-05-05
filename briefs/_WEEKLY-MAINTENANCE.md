# _WEEKLY-MAINTENANCE.md — The weekly architecture sweep

> One operator-triggered routine, run once a week, that keeps the workspace from drifting. Workers purge content (in their sandboxes); orchestrator handles structural changes (root MDs, `_config/`, memory, registries). Operator validates before any structural change ships.

---

## Cadence

Once a week. Suggested: **Sunday** (between-week buffer — no posting pressure, plenty of context from the week just ended). Operator-defined; pick a day and stick to it.

Trigger phrase: *"weekly maintenance"*, *"weekly sweep"*, *"weekly audit"*, or any equivalent.

---

## Roles

| Actor | What they do | What they do NOT do |
| --- | --- | --- |
| **Workers** (content-claude, design-claude, va, plus any custom workers) | Purge their own sandbox outputs. Archive completed briefs. Flag patterns they noticed (recurring edits, naming drift, repeated voice corrections). | Edit their own `CLAUDE.md` / `CONTEXT.md`. Touch `_config/`. Cross sandbox boundaries. |
| **Orchestrator** (this session) | Process worker flags into source-level fixes. Audit memory, `_config/`, registries. Update `CLAUDE.md` / `CONTEXT.md` / `_config/` / bootstrap as needed. Flag changes for operator validation. | Make structural changes without operator approval. Delete memory entries without surfacing them. |
| **Operator** | Validate proposed structural changes before they ship. Make business-decision calls (e.g. archive a project that's no longer active). Confirm the per-deliverable tracker matches actual platform reality. | Worker-level cleanup work — that's the workers' job. |

This matches the ICM **edit-source principle**: workers notice symptoms; orchestrator changes the source; operator validates.

---

## Routine (orchestrator runs in this order)

### Phase 1 — Worker purge dispatch (parallel)

For each active worker, write a small purge brief and dispatch to the worker's sandbox. The brief tells the worker:

- Archive completed briefs from this week into `briefs/done/`
- Move stale drafts (>7 days old, not posted, not in active brief) into `archive/`
- Walk their output folders; flag any orphaned files (no brief, no source, unclear purpose) in their session output
- List any recurring corrections / naming drift / voice issues they noticed during the week
- Do NOT modify CLAUDE.md, CONTEXT.md, `_config/`, or any cross-sandbox file
- Return: list of archived files, list of flagged patterns, list of any orphans found

Workers run in parallel — each takes a fresh session in their sandbox. Operator dispatches each one.

### Phase 2 — Orchestrator structural sweep (sequential, single session)

Once worker reports come back:

1. **Process worker flags into source fixes.** Invoke `/diagnose-recurring-edits` first — it aggregates breadcrumbs across all sandbox STATUS files + escalations from the last 14–30 days and surfaces patterns no single worker can see (per ICM § 6.3 edit-source loop). Then for each flagged pattern (worker-self or skill-detected): is the right fix to update `_config/BRAND.md` (voice rule), `_config/REFERENCE.md` (token / convention), `briefs/_BRIEF-TEMPLATE.md` (dispatch contract), or a sandbox CLAUDE.md (worker-specific guidance)? Draft the change. Do not apply yet.

2. **Audit memory.** Read `MEMORY.md` "Audit candidates" section. For each candidate: archive (move to `_archive/` subfolder), merge into another memory, or keep + remove the audit flag. Surface decisions to operator.

3. **Audit `_config/`.** Quick read of BRAND.md, REFERENCE.md, RELATED_PROJECTS.md. Is anything stale? Has any "Placeholder" been resolved this week and needs filling in? Has the brand evolved in ways the file doesn't reflect?

4. **Audit briefs/questions/.** Any unanswered questions from workers waiting for orchestrator response? Resolve or escalate to operator.

5. **Audit per-deliverable tracker.** Compare against this week's actual posts (operator confirms platform-level reality). Mark posted-confirmed items. Flag anything in the tracker as posted that operator didn't actually post. Flag anything operator posted that's not in the tracker.

6. **Audit calendar.** If a new week is starting Monday: pre-flight the calendar entries — every "READY" item has a real source file, every "WRITE" item has a brief queued, every reel cover has either an existing asset or a design-claude dispatch ready.

7. **Audit registries.** Are CLAUDE.md / CONTEXT.md / MEMORY.md all consistent with each other (sandbox lists, worker names, file paths)?

8. **Ideas inbox count.** Read `ideas.md`. Count tagged + untagged bullets pending. Surface in the report so the operator knows whether to run *"process ideas"* before or after this maintenance pass.

9. **Pattern observation (retrospective).** Read this week's `daily/YYYY-MM-DD.md` files (Mon–Sun). Extract:
   - Energy levels per day from each brief header
   - What was completed vs. slipped (validation checkboxes vs. tracker reality)
   - One pattern observed
   - One suggested adjustment for next week
   Append to `_log/RETROSPECTIVES.md` under the current week's date. Keep it tight — one short paragraph, not a treatise.

10. **Token-surface measurement.** Always-loaded files cost tokens every session. Measure and surface drift:
    - `wc -l` on user `MEMORY.md` — alert if approaching 180 lines (200-line silent truncation cap)
    - `wc -l` on root `CLAUDE.md` — alert if it grew >25% since last weekly sweep
    - `wc -l` on each sandbox `CLAUDE.md` and `CONTEXT.md` — same growth threshold
    - For any file flagged: surface candidate sections that could move to a route-discoverable location (`_config/`, sandbox CONTEXT.md, brief template) instead of staying always-loaded. Don't apply — surface for operator validation.

11. **Scan-surface measurement.** Per-scan files cost tokens every grep/list/read. For each sandbox, count file count in active output folders. Flag any folder with >10 active files. Suggest either subfolder split or `_archive/` move. Don't apply — surface for operator.

12. **First-Sunday-of-month trigger.** If today is the first Sunday of the calendar month, after weekly maintenance completes, run `briefs/_MONTHLY-MAINTENANCE.md` next. Surface to operator as the next routine to dispatch — do not auto-run it inside this session.

13. **Prune `.trash/` snapshots.** The `snapshot-before-edit.py` hook writes a start-of-day snapshot of high-blast-radius files to `.trash/YYYY-MM-DD/`. Delete any `.trash/<date>/` folders older than 30 days. Command: `find .trash -maxdepth 1 -type d -name '20*' -mtime +30 -exec rm -rf {} +` (run from project root). No operator validation needed — this is pure cleanup of safety-net copies that have aged past their useful window.

### Phase 3 — Operator validation gate

Orchestrator presents the proposed changes as a summary:

- Worker flags processed → source-level changes to apply (list)
- Memory candidates resolved (list)
- Per-deliverable tracker mismatches (list, requiring operator confirmation)
- briefs/questions/ resolutions (list)
- Calendar pre-flight gaps (list)
- Registry inconsistencies fixed (list)

Operator approves, edits, or rejects each. Orchestrator applies approved changes. Rejections + reasons get logged so we don't re-propose them next week.

### Phase 4 — Optional: workspace-builder runs

If a new worker is being added this week, run `briefs/_WORKSPACE-BUILDER.md`. Best done at end of weekly maintenance because the new worker enters the system clean, with all this week's source-level fixes already applied.

---

## Deliverables (what weekly maintenance produces)

- Cleaned sandboxes (workers' purge work, validated by their reports)
- Updated `_config/` files (voice / tokens / conventions reflect what's been learned)
- Pruned MEMORY.md (audit candidates resolved)
- Aligned per-deliverable tracker (matches platform reality)
- Cleared briefs/questions/ (no unanswered worker questions)
- Pre-flighted calendar for the upcoming week
- Operator-validated change log (one paragraph: "this week we changed X, archived Y, learned Z")

---

## Anti-patterns (don't do these)

- **Don't run weekly maintenance on the same day as heavy posting work.** It needs space; mixing it with execution work creates the kind of context drift that ICM is designed to prevent.
- **Don't let workers edit their own CLAUDE.md / CONTEXT.md.** Even small edits compound across sandboxes. Workers FLAG; orchestrator EDITS.
- **Don't apply structural changes without operator approval.** Speed isn't the bottleneck; alignment is.
- **Don't archive memory entries before the operator confirms.** Memories are cheap; surprised operators are expensive.
- **Don't extend Phase 2 to "while I'm at it" reorganizations.** If a bigger refactor is needed, that's its own dispatch, not part of weekly maintenance.

---

## Inputs (Layer 3 / Layer 4)

| Layer | File | Why |
| --- | --- | --- |
| 3 | `_config/BRAND.md` | voice rules to audit against worker flags |
| 3 | `_config/REFERENCE.md` | tokens / conventions to audit against worker flags |
| 4 | `MEMORY.md` (user memory) | audit candidates section |
| 4 | `briefs/questions/*.md` | unanswered worker questions |
| 4 | per-deliverable tracker | this week's posting log |
| 4 | This week's `daily/*.md` files | what was actually planned vs shipped |
| 4 | Worker reports from Phase 1 | flagged patterns + orphans |

---

## Verify (orchestrator runs before declaring weekly maintenance complete)

- [ ] Every worker dispatched in Phase 1 has returned a report
- [ ] Every worker flag from Phase 1 has been processed into either a source change, a non-action, or a deferred-decision note
- [ ] All `MEMORY.md` audit candidates have been resolved or explicitly deferred with a reason
- [ ] Per-deliverable tracker reconciliation has been confirmed by the operator (no orphan claims)
- [ ] All approved structural changes have been applied
- [ ] All rejected proposals are logged with the operator's reason (so they don't get re-proposed)
- [ ] Next week's calendar has no blocking gaps
- [ ] A one-paragraph change log has been written and shown to the operator
