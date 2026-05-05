# <slug> — Social-post Design Brief

*Handoff from content team to design team. Copy is locked. Build the assets.*
*Source: written by [content-claude / operator] via the content sandbox, finalised [YYYY-MM-DD] for [posting window].*

> **When to use this template:** any social-post output handed from content team to design team — single posts, carousels, memes, reel covers, story sets. NOT for article slides (use `articles/briefs/article-NN-design-brief.md` shape) or book/long-form covers (use `Book Cover/[Title]/*-Brief.md` shape).

---

## Brand reference (read first) — REQUIRED

Before building, the design team must read:

| File | Why it matters |
| --- | --- |
| `_config/REFERENCE.md` | Design Specs (sizes, backgrounds, overlay max), photo direction, palette, fonts, file naming |
| `design-claude/CONTEXT.md` | Background-direction rules. Current rule: see `_config/BRAND.md` design section |

Do NOT infer brand direction from rendered assets in legacy folders — many were produced before the current rules locked. The current rule lives in `_config/BRAND.md`; anything in those folders that contradicts it is legacy.

This brief inherits the palette and the photo direction from the docs above. The format-specific specs below extend, not replace, those docs. If a format-specific spec contradicts the brand docs, escalate — do not silently override.

---

## What this is

[1–2 paragraphs: type of post, the topic, what makes it interesting]

**Audience:** [who this is for — peer professionals? prospective customers? cold traffic? warm list?]

**Strategic role:** [what this post is supposed to do — drive sales, build trust, plant a seed, build authority, drive comments, etc.]

**Series fit (optional):** [if this is part of a series, which one + how it relates]

---

## Format specs

| Spec | Value |
| --- | --- |
| Canvas | [WxH px — see `_config/REFERENCE.md` Design Specs] |
| Format | [PNG / JPG] |
| Slide count | [N] |
| Output folder | `design-claude/[platform]/[subfolder]/[topic-slug]/` |
| File naming | per `_config/REFERENCE.md` "File Naming Conventions" |

---

## Visual direction

[Per-format visual notes. Reference brand tokens by name from `_config/REFERENCE.md`; don't redefine the palette / fonts here.]

- **Photos:** [if photos used — what direction, what to source from the photo library, any specific framing]
- **Type treatment:** [headline/body relationship, weight, scale]
- **Layout pattern:** [reuse an existing template script if one exists, name it; or describe the layout]
- **Color emphasis:** [which brand color carries this piece, if any specific accent matters]

If this brief departs from any `_config/REFERENCE.md` rule, name the rule and justify the exception in one line.

---

## Slide-by-slide / post-by-post

[Per-slide copy + visual direction. For carousels: one row per slide. For single posts: copy + visual direction in one block.]

| # | Copy | Visual direction |
| --- | --- | --- |
| 01 | [headline + body] | [layout, photo, accent] |
| 02 | [...] | [...] |
| ... | | |

---

## Hero slide / save-worthy slide (carousels only)

[Which slide is designed to be screenshotted, saved, or shared standalone? Design treats this as the visual peak — it earns extra weight, sharper composition, no body-text crowding.]

---

## Voice / copy locks

- Banned phrases: pull the canonical list from `_config/BRAND.md` § "Banned vocabulary" — do not duplicate here. The brief inherits the project's blocklist.
- Em-dash count ≤ 1 per slide
- Zero emojis
- Voice anchor: [link to the relevant voice rule in `_config/BRAND.md` or `_config/REFERENCE.md`]

---

## Acceptance

- [ ] All slides/posts at the spec size from `_config/REFERENCE.md`
- [ ] Brand palette applied (or brand exception explicitly justified above)
- [ ] Photo direction matches the brand rule — overlay ≤ spec max
- [ ] No legacy-asset patterns inadvertently copied (run a quick eyeball against `_config/REFERENCE.md` Design Specs table before declaring done)
- [ ] File naming matches `_config/REFERENCE.md` conventions
- [ ] Per-deliverable tracker updated under the right section
- [ ] [Any post-specific check, e.g., "hero slide reads at thumbnail"]

---

## Returns-with

- [ ] PNGs at the spec output folder
- [ ] One source file (HTML / JS / .ai / .fig) so re-renders don't require rebuilding from scratch
- [ ] Confirmation that the per-deliverable tracker is updated
- [ ] One short note (≤ 6 lines) on visual decisions made and anything to consider for the next brief in this format
