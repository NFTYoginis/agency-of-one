# _CALENDAR-TEMPLATE.md — Monthly calendar pattern

> Use this when building the next month's calendar. The goal is a **lean day-by-day post plan that's cheap to read every day**. Strategy, amplifiers, weekly rhythm, and rationale belong in a sibling `_log/<month>-strategy-and-amplifiers.md` file — never in the main calendar.

---

## When to run this

Trigger phrases: *"build [month] calendar"*, *"set up [month] calendar"*, *"new month calendar"*, or any equivalent.

Typically runs in the last week of the previous month, after Sunday weekly maintenance.

---

## What goes in `<MONTH>-CALENDAR.md` (the live, hot-path file)

Target: **150–250 lines** total. If it's longer, move surrounding content out.

**Required sections:**

1. **Title + 1-line intro pointing to the strategy file.**
2. **Status legend** (READY / WRITE / FILM / BUILD / POSTED).
3. **One section per week** — heading, 1–2 line theme, day-by-day post table.
4. **References table** linking to: strategy file, status file, source-file conventions, future-month template, archive snapshots.

**Daily-posts table columns:**

| Date | Post / Action | Channel | Status |

That's it. If a row needs writer guidance (cold-traffic angle, caption reframe, etc.), inline it inside the "Post / Action" cell — the row is the writer's brief.

**Source paths inline:** for READY posts, link to the source file directly in the row (`(content-claude/posts/x.md)` etc.) so the daily-brief generator can grep one row and have everything it needs.

**Acceptable in-table extras:** VA checklist for launch/build weeks (when build dependencies live in the calendar — that's appropriate). Keep it tight.

---

## What goes in `_log/<month>-strategy-and-amplifiers.md` (off-hot-path)

Anything strategic, one-time-read, or referenced rarely:

- **The Big Picture** — why this month, the 3 jobs, the framing
- **Five Rules** style orientation lists
- **Where to Post** / cross-posting rules (only if changed; otherwise skip — it's stable)
- **Filming / production schedules** with rationale per day
- **Free-asset / lead-magnet systems** with product mappings
- **Weekly Rhythm** template
- **Habit-tracking topics** for the month
- **Amplifiers Layer** — paid boost calendar, outreach ritual, podcast pitches, list-priming sequences
- **Conversion Checklists**
- Long-form footnotes / change logs

Loaded only when planning, validating amplifiers, or auditing strategy. **Never read during a daily-brief generation.**

---

## What goes in `_archive/<MONTH>-CALENDAR-pre-trim.md` (audit trail)

If you're rewriting an existing calendar (rather than starting fresh), copy the original here first. Filename pattern: `<MONTH>-CALENDAR-YYYY-MM-DD-pre-trim.md`. Never delete the original — archive it.

---

## What goes in the per-deliverable tracker (separate file, single source of truth)

Posted vs not-yet-posted. The calendar marks **planned** status (READY/WRITE/FILM/BUILD); the per-deliverable tracker marks **shipped** status (POSTED with date). Don't duplicate. The auto-stamp hook keeps the date line current on edits.

---

## What goes in NO file (delete on every monthly rewrite)

These produce token cost without earning their place on the hot path:

- "What's Already Built" inventories — duplicates the per-deliverable tracker
- "What Needs to Be Written" tables — duplicates the WRITE rows in daily tables
- "What Needs to Be Filmed / Produced" tables — duplicates the FILM/BUILD rows
- Past-month warmup days — gone the moment the month starts

If you need a "what's pending" view at any point, read the per-deliverable tracker and grep the calendar for non-POSTED rows. Don't maintain a parallel list.

---

## Step-by-step: build a new monthly calendar

1. **Copy this template's structure** into a new `<MONTH>-CALENDAR.md` at project root.
2. **Define the 4 (or 5) weekly themes** — one line each.
3. **Build the daily-posts table for each week.** Pull dates from a calendar widget so weekday alignment is right. Inline source paths for READY rows.
4. **Decide what's in scope this month for amplifiers.** Confirm with operator.
5. **Create `_log/<month>-strategy-and-amplifiers.md`** with: Big Picture, Filming schedule, Free Asset / Course Mapping, Weekly Rhythm, Habit-tracking topics, Amplifiers (active/deferred status), Conversion Checklist.
6. **Update `MEMORY.md`** orchestrator memory with a one-line note: "[Month] calendar built — file pattern: lean day-by-day + sibling strategy file."
7. **Confirm with operator** before declaring the calendar "live."

---

## Anti-patterns

- **Don't push amplifier detail back into the calendar.** It always grows back. The strategy file is the only place for it.
- **Don't inline 3-paragraph rationales in daily-post rows.** One-line cues only. If a writer needs more, link to the source brief file.
- **Don't track posted/not-posted status in the calendar.** Only PLANNED status. Posted lives in the per-deliverable tracker (auto-stamped).
- **Don't keep "Where to Post" or "Status System" sections in every monthly calendar.** Stable rules — they live in `_config/REFERENCE.md` or are inferred from column conventions. Surface them once at month-start in the strategy file if anything changed.
- **Don't carry past months' content into the new calendar.** Each month is a clean file. End-of-month, archive the spent calendar.

---

## Verify (orchestrator runs before declaring the new calendar live)

- [ ] Calendar file is under 250 lines
- [ ] Every week has a daily-posts table with all 7 days
- [ ] Every READY row has an inline source-file path
- [ ] No "What's Already Built" / "What Needs Written" / "What Needs Filmed" tables in the calendar
- [ ] Strategy file exists and contains the moved content
- [ ] Previous month's calendar archived
- [ ] References table at calendar bottom links to strategy + tracker + archive
- [ ] Operator approved
