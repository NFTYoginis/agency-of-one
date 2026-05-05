# _PASTE-SNIPPETS.md — Canonical paste-templates for daily dispatch

> The two paste-templates + pre-flight checklist used on every routine `execute [date]` / `prep today` run. Load this file alone for routine dispatches; load `_TODAY-TEMPLATE.md` only on full-brief mode, rule changes, or first-time orchestrator onboarding.

---

## Pre-flight checklist (run BEFORE writing any dispatch)

For today's calendar row, decide:

1. **Slug** — derived from the calendar row's topic (snake_case).
2. **Caption MD exists?** Check `../content-claude/posts/[slug]-post.md`.
   - **NO** → parallel-dispatch content-claude + design-claude (two prompts, single operator paste action).
   - **YES** → design-claude only.
3. **Cover PNG exists?** Check `design-claude/final/[brand]_cover_[slug].png` AND `..._oldstyle.png`.
   - **NO** → BUILD path (full design-claude prompt below).
   - **YES** → REFRESH-only path (dashboard + caption-embed only; skip cover render).
4. **Photo source** — calendar row names it OR an obvious `assets/photos/[folder]/` exists OR defer to `design-claude-pick`.

`operator-live` is **not** an option for caption on feed posts. Reserved for Stories / ephemeral formats only.

---

## Snippet A — design-claude (covers + dashboard, BUILD path)

> *Read `design-claude/CLAUDE.md`, `../_config/REFERENCE.md`, and `../briefs/_WEEKLY-HTML-TEMPLATE.md`. Two deliverables in a single pass.*
>
> *Pre-decided fields:*
> - *date: [DATE — Weekday, Month Day]*
> - *calendar row: `[VERBATIM ROW]`*
> - *phrase: "[VERBATIM HEADLINE — line1/2/3 + subline if from generate_cover.js entry]"*
> - *slug: `[slug]`*
> - *category: `[CATEGORY]`*
> - *caption: `../content-claude/posts/[slug]-post.md`*
> - *photo: `../assets/photos/[folder]/[file].jpg]` OR `design-claude-pick`*
>
> *1. **Reel covers (2-cover convention).** Output `final/[brand]_cover_[slug]_oldstyle.png` (oldstyle text-only — text-only generator if entry exists in `scripts/utilities/generate_cover.js`) and `final/[brand]_cover_[slug].png` (photo-driven editorial). Both at the brand spec size, brand palette. Bright high-key always — never dark/moody. Verify headline fits the spec safe zone. Verify the brand handle has contrast against the photo region — add a soft scrim if needed.*
>
> *2. **Weekly dashboard.** Update `../daily/THIS-WEEK.html` per `../briefs/_WEEKLY-HTML-TEMPLATE.md`. Single-pass: embed real cover previews from #1; embed caption block verbatim from the post MD. If existing dashboard header is in a prior week, rebuild from scratch. Otherwise refresh today's section in place and roll prior-day cards into "Earlier this week." Source links go to calendar row or caption MD. Self-contained HTML.*
>
> *Return both file paths when done.*

**REFRESH-only variant:** drop deliverable #1; deliverable #2 reads existing PNGs + freshly-written caption MD only.

---

## Snippet B — content-claude (caption MD)

> *Read `content-claude/CLAUDE.md` + the closest-sibling exemplar `posts/[exemplar-filename].md` (same audience, same format — copy its structure).*
>
> *Write `posts/[slug]-post.md`.*
>
> - *topic: [topic line]*
> - *slug: `[slug]`*
> - *category: `[CATEGORY]`*
> - *hook context: cover headline reads "[headline]" subline "[subline]"*
>
> *Match exemplar format exactly: YAML frontmatter (topic, platform, audience, slug, category) → confronting hook (1–2 lines, name ONE specific [domain] pattern) → 3 short concrete examples of [the alternative behavior] → close with a single brand-voice line about [angle] → 5-cap hashtag block (no own-brand tags — see brand list).*
>
> *Add a row to the per-deliverable tracker immediately on creation (status: Ready). Return file path.*

---

## Parallel-dispatch handoff sentence to operator

> *Two paste-prompts (Snippet B above for content-claude, Snippet A above for design-claude). Run them in parallel — content-claude writes the caption MD while design-claude builds covers. design-claude embeds the caption verbatim once the MD lands.*

---

## Hard rules (still apply — don't drop)

- **Cheap is default.** Routine daily ≈ 5–10k tokens. If you find yourself reading more than the calendar row + maybe 1 supporting grep, stop.
- **Worker boundary** — content-claude does captions only on the daily flow (no HTML, no visuals). design-claude does covers + dashboard. Orchestrator dispatches.
- **`../` paths in dispatch prompts** — workers' CWD is their sandbox.
- **Update STATUS.md** at end of any session that ships, dispatches, or shifts a thread.
