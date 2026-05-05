# _TODAY-TEMPLATE.md — Daily dispatch (cheap mode default)

> Calendar is already complete. design-claude maintains a single rolling `daily/THIS-WEEK.html` dashboard — refreshed each dispatch. Orchestrator's only job: grep the calendar row, write the worker prompt, hand off. **Target cost per day: <10k tokens.**

> **Routine days: load `_PASTE-SNIPPETS.md` instead of this file.** The two paste-templates (design-claude + content-claude) and the pre-flight checklist live there as a small canonical file (~80 lines). This file (`_TODAY-TEMPLATE.md`) is the full spec — load only on full-brief mode, rule changes, or first-time orchestrator onboarding.

---

## Trigger phrases

*"prep today"* · *"today's plan"* · *"daily brief"* · *"execute [date]"* · *"what am I doing today"*

---

## Default mode: dispatch-only

Use this for any day where the calendar row is unambiguous. This is **almost every day**.

### Steps

1. **Grep one row.** `grep -n "[Date label]" [active calendar].md`. Read the row + adjacent context only — typically 3–5 lines. Do NOT load the full week, the strategy file, or prior-day artifacts.
2. **Identify the worker(s) needed.** Most days = design-claude (cover + weekly dashboard refresh). Some days = none (operator manual). Some days = content-claude (writing). Read it directly off the row.
3. **Write the dispatch prompt inline in chat.** Do NOT generate a daily MD file. The worker is the artifact owner.
4. **Hand off.** One sentence to the operator: prompt is ready, paste into a fresh worker session.

### What you do NOT do in default mode

- Do **not** read prior-day MDs or `daily/THIS-WEEK.html` — design-claude reads the dashboard itself when refreshing
- Do **not** read source files (scripts, post copy, article briefs) — operator opens those at execution time
- Do **not** read the full week section, strategy file, or REFERENCE.md unless the dispatch prompt genuinely needs a token from it
- Do **not** generate `daily/YYYY-MM-DD.md` — the rolling weekly HTML is the artifact
- Do **not** generate per-day HTMLs (`daily/YYYY-MM-DD.html`) — the rolling `daily/THIS-WEEK.html` is the only dashboard file
- Do **not** enumerate validation checklists, Plan B, or operator notes — those live in the dashboard if needed
- Do **not** ask about energy level on a routine day — that's a full-brief-mode question

### Standard design-claude dispatch (paste-template)

Paths use `../` because design-claude's CWD is `design-claude/`. Bare paths (`daily/...`, `_config/...`) break from inside the design sandbox — always prefix with `../` for cross-sandbox reads.

**Required pre-decided fields (orchestrator decides; never defer to worker):**

| Field | What it is | Source |
| --- | --- | --- |
| `date` | Day being dispatched | Calendar row date label |
| `calendar row` | Verbatim row text | Active month's calendar |
| `phrase` | Exact verbatim Key Phrase that becomes the cover headline | `_config/REFERENCE.md` Key Phrases — orchestrator picks one |
| `slug` | Filename slug (snake_case) | Orchestrator derives from phrase |
| `category` | Category tag (e.g., `CRAFT`, `PRACTICE`, `THEORY`) | Orchestrator picks from existing tag conventions |
| `caption` | Path to post MD at `../content-claude/posts/[slug]-post.md` — design embeds verbatim. **MD must exist before design-claude renders the dashboard.** If missing, dispatch content-claude IN PARALLEL with design-claude (two prompts in the same operator paste action). `operator-live` is reserved for genuinely caption-less formats (Stories, ephemeral content) — **never the default for reel covers or feed posts**. | Orchestrator checks `../content-claude/posts/` first; if missing, parallel-dispatch content-claude using the format-match pattern: point worker at the closest-sibling exemplar MD + pre-decided slug/category/hook |
| `photo` | One of: `<path-to-photo-file>` OR `design-claude-pick` (worker curates from the photo library) | Orchestrator names the photo when calendar topic implies an obvious source folder; otherwise defers |

Why this matters: deferring `phrase` / `slug` / `category` to design-claude burns worker context on a creative branch the calendar already implicitly decides. Orchestrator picks them in ~50 tokens; worker would spend ~2k tokens reading REFERENCE.md and reasoning about angles.

**Paste-template:**

> *Read `design-claude/CLAUDE.md`, `../_config/REFERENCE.md`, and `../briefs/_WEEKLY-HTML-TEMPLATE.md`. Two deliverables in a single pass:*
>
> *Pre-decided fields:*
> - *date: [DATE]*
> - *calendar row: "[VERBATIM ROW]"*
> - *phrase: "[VERBATIM KEY PHRASE FROM REFERENCE.md]"*
> - *slug: `[snake_case_slug]`*
> - *category: `[CATEGORY_TAG]`*
> - *caption: `[../content-claude/posts/[slug]-post.md]` OR `operator-live`*
> - *photo: `[../assets/photos/[folder]/[file].jpg]` OR `design-claude-pick`*
>
> *1. **Reel covers (2-cover convention).** Output `final/[brand]_cover_[slug]_oldstyle.png` (oldstyle text-only) and `final/[brand]_cover_[slug].png` (photo-driven editorial). Both at the brand spec size, brand palette.*
>
> *2. **Weekly dashboard.** Update `../daily/THIS-WEEK.html` per `../briefs/_WEEKLY-HTML-TEMPLATE.md`. Single-pass: embed the real cover previews you just produced — no `.pending-tile` placeholders, no second-pass regen. If the existing file's header date is in a prior week, rebuild from scratch. Otherwise, refresh today's section in place and roll prior-day cards into "Earlier this week."*
>
> *Source links in the dashboard go to the calendar row or to the caption source MD — never to per-day daily MDs (those don't exist in the default flow). Self-contained HTML — no external CSS/JS.*
>
> *Return both file paths when done.*

Adjust per row: no-cover days drop deliverable 1; film-only days may dispatch the dashboard refresh only; if `caption: operator-live`, design-claude renders the card without a caption block. **Keep the prompt under 250 words.**

**Worker boundary** (per `_config/_WORKER-RULES.md` § 9): on the default daily flow, content-claude does NOT produce HTML or visuals. content-claude DOES produce caption MDs when the post MD for today's slug doesn't yet exist — parallel dispatch with design-claude, single operator paste action. Don't have orchestrator generate HTML directly.

---

## Opt-in mode: full brief

Use **only** when:
- The operator explicitly says *"full brief"* / *"detailed plan"* / *"inline content"*, OR
- The calendar row is genuinely ambiguous (vague entry with multiple candidate angles + no clear default, OR a worker dispatch needs upstream decisions the operator hasn't made)

In full-brief mode, generate `daily/YYYY-MM-DD.md` with the structure below. **Reference, don't inline.** Keep under 250 lines.

```markdown
# TODAY — [Weekday], [Month] [Day], [Year]

**Week:** [week label]
**Week theme:** [one line]
**Energy:** [High / Med / Low — operator-stated]

## What's on today

| # | Deliverable | Type | Worker | Status |
| --- | --- | --- | --- | --- |

## [Per-deliverable sections — 2–3 line summary, source path, dispatch action]

## Plan B *(only if energy is Med or Low)*

## Workers active today

## Validation before posting

## Tomorrow (preview)

## Operator notes
```

---

## Hard rules

- **Cheap is default.** A routine daily execution should be ~5–10k tokens, not 50k. If you find yourself reading more than the calendar row + maybe 1 supporting grep, stop and confirm full-brief mode was actually requested.
- **Worker owns the artifact.** design-claude maintains `daily/THIS-WEEK.html`. Orchestrator does not duplicate that work in MD or generate the HTML directly.
- **Prior-day rollover is the worker's job.** Orchestrator does not read prior-day MDs or the dashboard HTML.
- **No speculative source-file reads.** Operator opens scripts, post copy, etc. at execution time. The orchestrator only reads a source file if the dispatch prompt itself can't be written without it.
- **One rolling weekly HTML — no per-day HTMLs.**
- **Past full-brief MDs remain as a log.** Don't edit them.
- **Don't update the per-deliverable tracker from this routine.** That update happens after the operator confirms a post is live.
- **Use `../` paths in dispatch prompts.** Workers' CWD is their sandbox, not the project root.
