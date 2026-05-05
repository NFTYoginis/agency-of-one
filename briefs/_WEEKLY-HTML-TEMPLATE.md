# _WEEKLY-HTML-TEMPLATE.md — Rolling weekly dashboard (design-claude)

> A single rolling HTML dashboard for the active week. Pairs with the calendar. Purpose: let the operator scan today's assets at a glance and verify earlier-this-week items shipped — without generating seven HTMLs per week.

---

## File location and lifecycle

**Path:** `daily/THIS-WEEK.html` — single rolling file. Always represents the current calendar week.

**Regenerated:** On every design-claude dispatch (i.e., whenever new covers or assets ship — typically 3–4× per week).

**Week reset:** On the first dispatch of a new week (Monday-or-later first dispatch), design-claude detects the week boundary and starts the file fresh. Prior week is not preserved as a file — the calendar and per-deliverable tracker are the historical log. The dashboard is a working surface, not an archive.

**Detection rule:** if the existing `THIS-WEEK.html` header date is in a prior calendar week (Mon–Sun) compared to today, treat it as stale and rebuild from scratch. Otherwise, append/refresh in place.

---

## Structure (two sections, in this order)

### Section 1 — Today

The dispatch date. Renders every deliverable design-claude produced in this dispatch + any other deliverables the calendar assigns to today. For each:

- **Title and goal** — pulled from the calendar row
- **Asset preview** — embed the cover/slide/thumbnail you produced in *this* dispatch as `<img>` with a relative path. **Real preview, single pass.** Never ship the dashboard with `.pending-tile` placeholders, "asset coming" text, or any other pre-render stub. If no visual exists for the card, render the text content (post copy, script hook, caption) inside a styled blockquote — but never a placeholder for a visual that's about to exist.
- **Caption + hashtags handling — driven by the dispatch `caption` field:**
  - If dispatch says `caption: <path-to-source-md>` → embed verbatim from that file. Hashtag line on the last line, bolded. **Hard cap: 5 hashtags. Keyword-only — exclude own-brand tags (carried by the handle + bio, not hashtags).**
  - If dispatch says `caption: operator-live` → omit the caption block entirely. The card is image + channel tag only. Operator types caption live at post time.
  - If neither field is set → escalate to orchestrator. Never invent caption copy.
- **Channel tag** — small label, accent color
- **Source link** — anchor to the relevant calendar section, the caption source MD, or the article brief. **Never to a per-day daily MD** (`daily/YYYY-MM-DD.md`) — those only exist in opt-in full-brief mode. If no useful source exists, omit the link entirely.

### Section 2 — Earlier this week

Every day in the active week prior to today, **most recent first**. For each prior day:

- **Day header** — e.g., *Monday, May 4*
- **Shipped cards** — same card layout as today's cards, but compressed and rendered with checklist state instead of a fresh dispatch view:
  - `[ ] Posted to [platform]`
  - `[ ] Confirmed live`
  - `[ ] Per-deliverable tracker updated`
- Visually distinct from today — alternate background versus today's primary background.

If a prior day has no design deliverables (filming-only or rest day), render a single line: *"Production day — no posted assets."* Do not omit the day.

**On the first day of a week (Monday's first dispatch):** Section 2 is empty — render a single line *"First day of the week. Earlier-this-week section empties on Monday."* and continue with Section 1 only.

---

## Visual styling

Match brand tokens from `_config/REFERENCE.md`:

| Element | Value |
| --- | --- |
| Body background | per `_config/REFERENCE.md` primary |
| "Earlier this week" section background | per `_config/REFERENCE.md` alternate |
| Body text | per brand body color, font: brand body or system sans-serif fallback |
| Headings | per brand headline color, font: brand headline or system serif fallback |
| Week label / category tags | accent color, uppercase, letter-spaced |
| Source links | accent secondary |
| Checked checklist items | accent secondary checkmark |
| Card borders | brand-subtle border |
| Card padding | 24px |
| Card border-radius | 8px |
| Page padding | 40px |

No dark backgrounds. No gradients. No JS. No external CSS imports — embed all styling inline in `<style>` block within `<head>`.

Images sized to `max-width: 240px` for in-page preview. Click-through to full image via `<a href="path/to/image.png">`.

---

## Self-contained rule

The HTML must open and render correctly with no internet connection and no external assets beyond images stored inside the project folder. Image paths use relative references from `daily/` (e.g. `../design-claude/final/[brand]_cover_topic.png`).

---

## "Missed item" pattern

The Earlier-this-week section is the missed-item check. Checklists default to *unchecked*. The operator marks `[x]` manually, or design-claude marks them based on operator confirmation in the next dispatch. Items with no posted-live confirmation by the next dispatch display with `(unconfirmed)` in accent — visible but not alarming.

---

## What design-claude does NOT do in this file

- Does not generate new copy or rewrite captions — pulls verbatim from the source post MD specified in the dispatch's `caption` field, or omits the caption block entirely if `caption: operator-live`
- Does not invent captions or hashtags. If `caption` field is missing or ambiguous, escalate — do not guess
- Does not modify the calendar or any source MD
- Does not create assets that aren't already specified in the calendar or already in the project
- Does not add anything beyond Section 1 and Section 2 (no "tomorrow preview" — that's already in the calendar)
- Does not ship `.pending-tile` placeholders or any pre-render stub. Dashboard is single-pass: covers are produced, then immediately embedded as real previews. No two-pass regen pattern.
- Does not link to per-day daily MDs (`daily/YYYY-MM-DD.md`). Those don't exist in the default flow.
- Does not preserve the prior week. Week boundary = full rebuild, no merge.

---

## Cover deliverables — 2-cover convention (design-claude applies by default)

When the calendar calls for a reel cover (`Any reel cover — [angle]`), design-claude ships **two** variants on the same topic — both belong in the grid:

1. **Oldstyle text-only** — `final/[brand]_cover_[slug]_oldstyle.png`. Solid brand background, brand SVG layout following the text-only generator. Sharp + SVG, no AI generation cost.
2. **Photo-driven editorial** — `final/[brand]_cover_[slug].png`. Photo background + dark gradient + overlay typography. Headline kept inside the platform safe zone.

Both at the brand spec size, brand palette. Headline copy taken verbatim or near-verbatim from `../_config/REFERENCE.md` Key Phrases.

**The orchestrator's dispatch prompt does not need to specify "two covers" — design-claude applies this convention by default.** The prompt only specifies the topic angle. If only one variant is wanted for a specific reason, the prompt must explicitly say so.

The dashboard embeds both variants side-by-side under the cover deliverable card.

---

## Path conventions for cross-sandbox reads

design-claude's working directory is `design-claude/`. Files outside that sandbox use `../` prefix:

| Reference | Path from design-claude CWD |
| --- | --- |
| Project root configs | `../_config/REFERENCE.md` |
| Briefs | `../briefs/_WEEKLY-HTML-TEMPLATE.md` |
| Calendar | `../<MONTH>-CALENDAR.md` (current month) |
| Daily folder | `../daily/THIS-WEEK.html` |
| Source post MDs | `../content-claude/posts/[slug].md` |
| Photo library | `../assets/photos/` (or wherever the operator stores them) |

The dashboard's own embedded image paths are relative *from* `daily/`, not from design-claude's CWD — i.e., `../design-claude/final/...`. This is correct because the HTML opens from `daily/` in the browser.

---

## Boilerplate dispatch prompt (orchestrator → design-claude)

The canonical dispatch template lives in `../briefs/_TODAY-TEMPLATE.md` (Standard design-claude dispatch section). It includes the seven required pre-decided fields (date, calendar row, phrase, slug, category, caption, photo) — orchestrator fills them in before dispatching. Do not re-derive the prompt from this template; copy the one in `_TODAY-TEMPLATE.md`.

Dashboard-only dispatch (no new cover work today, but operator wants the dashboard refreshed):

> *Read `../briefs/_WEEKLY-HTML-TEMPLATE.md`. Update `../daily/THIS-WEEK.html` — refresh today's section based on the calendar row for [DATE], roll prior-day cards into "Earlier this week." No new asset generation. Return the file path when done.*
