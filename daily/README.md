# daily/

The rolling weekly dashboard lives here.

**`THIS-WEEK.html`** — single rolling HTML file produced and refreshed by design-claude on every dispatch. Always represents the current calendar week. On Monday's first dispatch, design-claude detects the week boundary and rebuilds from scratch.

**Pattern reference:** `../briefs/_WEEKLY-HTML-TEMPLATE.md`. The dispatch routine that drives each refresh: `../briefs/_TODAY-TEMPLATE.md` and `../briefs/_PASTE-SNIPPETS.md`.

**Why one rolling file (not seven per week):** the dashboard is a *working surface*, not an archive. The historical log lives in:

- The active month's `<MONTH>-CALENDAR.md` (planned)
- The per-deliverable tracker (e.g., `CONTENT-STATUS.md`) (shipped)

Per-day HTMLs (`daily/YYYY-MM-DD.html`) are an anti-pattern — see `../_config/COMMON-MISTAKES.md` § 1b.

**Full-brief mode (opt-in):** when the operator says *"full brief"*, the orchestrator generates `daily/YYYY-MM-DD.md`. These exist as a log; no worker reads them on subsequent dispatches. Default flow is HTML-only; MDs are the exception.

**This README ships empty in the template** — the first `THIS-WEEK.html` is generated the first time design-claude is dispatched.
