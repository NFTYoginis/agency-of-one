# design-claude — Context

Design environment. Read this after CLAUDE.md. It tells you what's currently being built and what to load per task.

---

## Reference Exemplars — calibrate against the real thing

Adjective-based design rules drift. Concrete exemplars don't. Before building in any format, open the canonical reference for that format. After rendering, eyeball your output against it: same chrome? same typographic weight? same overlay opacity? If not, the gap is the redo target.

For design, the exemplar is two things paired: the rendered PNG (visual calibration) and the script that produced it (implementation reference). Forking the script is usually the right starting move.

| Format | Canonical exemplar (PNG · script) | What it demonstrates |
| --- | --- | --- |
| Article slide deck | _TBD — orchestrator nominates once first canonical piece ships_ | [Placeholder: photo-backed 10-slide spine, brand-tag/slide-counter chrome, headline auto-sizing.] |
| Thumbnail | _TBD_ | [Placeholder: aspect, gradient direction, photo placement, text crop logic.] |
| Story (vertical) | _TBD_ | [Placeholder: gradient bottom 45%, handle top-left, content bottom-anchored.] |
| Editorial split-quote cover | _TBD_ | [Placeholder: side blocks + big serif emphasis word + tagline.] |
| Labeled body-map / diagram | _TBD_ | [Placeholder: figure + connector arcs to labeled regions.] |
| Illustration card | _TBD_ | [Placeholder: card spec — frame, glow, terminal markers, typography.] |
| Book cover (full wrap) | _TBD_ | [Placeholder: series visual family — palette, type pair, back-cover treatment.] |
| Reel cover (text-only, fallback) | `scripts/utilities/generate_cover.js` (or equivalent) | Last-resort fallback only. Use when no visual fits. Not the default. |

> **Orchestrator note:** one canonical reference per format. Update only when a clearly stronger piece ships. Do not let this become a "good examples" list. Workers comparing against three exemplars get diffuse output; workers comparing against one get tight output.

---

## What to Load for Each Design Task

| Task | Load first | Then |
| --- | --- | --- |
| Article slides / thumbnail / story | Brief in `articles/briefs/article-[nn]-design-brief.md` | Run `scripts/article-[nn].js` |
| Reel / social cover | Read post topic first → decide CREATE (image-gen) or CURATE (existing photo asset) | Memory: `feedback_covers_with_visuals.md` (if present) · template scripts in `scripts/experiments/` |
| Text-only reel cover (fallback) | Root `_config/REFERENCE.md` → Design Specs + Naming | Edit `scripts/utilities/generate_cover.js` variables — only when no visual fits |
| Editorial split-quote image | `scripts/experiments/split-quote-experiment.js` (when you've built one) | Memory: `project_quote_image_format.md` for layout math |
| Labeled diagram image | `scripts/experiments/body-map-experiment.js` (when you've built one) | Memory: `project_body_map_format.md` |
| Illustration / card | `illustrations/briefs/DESIGN-[topic]-Illustration-Brief.md` | HTML reference map in same folder |
| Book / long-form cover | Brief in `Book Cover/[Title]/` | `BOOK-LAYOUT-Reference.md` for component system (when you've built one) |
| Platform asset (Kajabi / Vimeo / etc.) | Root `_config/REFERENCE.md` → Design Specs | Brand-specific platform brief |

---

## Current Design Priorities

[Placeholder: 4–6 lines. What's the top thing pending in this sandbox right now? Operator refreshes monthly.]

1. _no active priorities — awaiting first dispatch_

---

## Background Direction — All Future Work

Defer to `../_config/BRAND.md` § 6 and § 7. Anything in that file overrides anything inline here. The general anchor (operator may override): bright, luminous, light and airy. Not dark, not moody, not editorial-heavy.

- Solid-color pieces: backgrounds per `../_config/REFERENCE.md`
- Photo-backed pieces: high-key photos, outdoor light, natural settings, warm daylight (adjust per brand)
- Overlay opacity: max per `../_config/REFERENCE.md` Design Specs
- Never darken a slide to compensate for a weak photo — pick a better photo
