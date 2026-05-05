# Monthly Audit Log

> Run on the **first weekly maintenance of each calendar month** (per `_WEEKLY-MAINTENANCE.md` Phase 2 token-surface step). For each tracked addition, confirm it's still being used and decide: **keep** (still useful), **adapt** (modify), or **retire** (no longer earning its complexity).
>
> Adding new architectural changes? Append them to the **Tracked additions** table below with a `created` date. Future audits will pick them up automatically.

---

## How to audit

For each row in **Tracked additions**, the orchestrator checks:

1. **Activity signal.** Has the file/feature been touched, populated, or referenced this month?
   - `ideas.md` → has the inbox been written to or processed?
   - `_log/RETROSPECTIVES.md` → are weekly entries being appended?
   - Energy field in daily briefs → are operators stating energy levels?
   - Hooks → have they fired (the side effect is observable in tracker dates and handoff-file edit attempts)?
2. **Friction signal.** Has the operator explicitly asked to skip, override, or work around the feature this month?
3. **Verdict.** Keep / Adapt / Retire. If Adapt, draft the proposed change. If Retire, surface for operator confirmation before removing.

Append a new row to the **Audit history** table for each month audited.

---

## Tracked additions

> Example structure — replace with real entries as you add architectural changes. Each entry has an ID, name, files changed, date created, and one-line "why it exists."

| ID | Addition | Files | Created | Why it exists |
| --- | --- | --- | --- | --- |
| A1 | _example: ideas inbox + processing_ | `ideas.md`, `briefs/_IDEAS-PROCESSING.md` | YYYY-MM-DD | _capture stray thoughts before they're lost in chat_ |
| A2 | _example: snapshot-before-edit hook_ | `.claude/hooks/snapshot-before-edit.py`, `.claude/settings.json` | YYYY-MM-DD | _start-of-day safety net for high-blast-radius file edits_ |

*To add a new tracked addition: append a row with the next ID and today's date. Don't renumber existing rows.*

---

## Audit history

One row per month audited. Date = the day audit was actually run. Verdicts: ✓ keep · ⚠ adapt · ✗ retire · — not yet evaluated (created mid-month, audit next month).

| Audit date | A1 | A2 | Notes |
| --- | --- | --- | --- |
| _YYYY-MM-DD (first weekly of [month])_ | — | — | _placeholder — first audit row goes here once the routine fires_ |

*Append future audit rows above this line. Use one column per tracked addition. If a column ever shows ✗ retire and the operator confirms removal, drop the column from future rows and note the retirement in the row's Notes column.*

---

## Retirement protocol

If an addition is retired:

1. Remove the file(s) listed in the **Tracked additions** row.
2. Remove the trigger / step references in CLAUDE.md, CONTEXT.md, and `_WEEKLY-MAINTENANCE.md`.
3. Mark the **Tracked additions** row with `RETIRED YYYY-MM-DD` in a new "Retired" column (add the column on first retirement).
4. Stop tracking it in **Audit history** rows going forward.
5. Note the reason briefly so we don't re-add the same idea blindly later.
