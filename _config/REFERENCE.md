# REFERENCE.md — Brand Reference

Quick lookups. No prose. Open this when you need a spec, not a file.

---

## Colors

[Placeholder: brand color table. Example structure:]

| Name | Hex | Use |
| --- | --- | --- |
| Background (primary) | `#______` | All design work |
| Background (alternate) | `#______` | Alternate across grid |
| Accent (primary) | `#______` | Buttons, CTAs, energy |
| Accent (secondary) | `#______` | Premium / category-specific contexts |
| Body text | `#______` | — |
| Headline | `#______` | — |

---

## Fonts

[Placeholder: brand font pair. Example structure:]

| Use | Font |
| --- | --- |
| Headings | [Placeholder: e.g. Playfair Display] |
| Body / labels | [Placeholder: e.g. Lato] |
| Technical exception (if any) | [Placeholder: e.g. Inter base64-embedded for Puppeteer rendering — name the technical constraint that forced the exception] |

---

## Design Specs

[Placeholder: per-output-format spec table. Example structure:]

| Output | Size | Background | Overlay max |
| --- | --- | --- | --- |
| [Format 1, e.g. reel covers] | [Placeholder: WxH px] | [Placeholder: hex or "AI photo"] | [Placeholder: e.g. 0.40] |
| [Format 2] | [Placeholder] | [Placeholder] | [Placeholder] |
| [Format 3] | [Placeholder] | [Placeholder] | [Placeholder] |

Photo direction: [Placeholder: one-line summary of allowed photo style — e.g. "outdoor light, natural settings, warm daylight. Never dark, moody, or studio-heavy."]

---

## Product Prices

[Placeholder: pricing table for the brand's products. Used by content workers writing CTAs and promotional copy so prices stay consistent across the funnel.]

| Product | Regular | Sale |
| --- | --- | --- |
| [Placeholder: product 1] | $— | $— |
| [Placeholder: product 2] | $— | $— |

---

## Tags / Segments

[Placeholder: any segmentation tags used by the email/CRM platform. List as-is so workers writing automations or broadcast copy reference real tag names.]

`[Placeholder: tag-1]` · `[Placeholder: tag-2]` · `[Placeholder: tag-3]`

---

## Platform Handles

[Placeholder: every social handle and primary URL the brand owns. The contact email here is the one workers reference when generating signatures or contact blocks.]

| Platform | Handle / URL |
| --- | --- |
| [Placeholder: platform 1] | @[Placeholder] |
| [Placeholder: platform 2] | @[Placeholder] |
| Email | [Placeholder: contact@example.com] |

---

## Key Phrases (use verbatim — do not paraphrase)

[Placeholder: locked phrases. Same list as `BRAND.md` § 4 — duplicated here for fast lookup. Workers reference whichever file they have open.]

- "[Placeholder: locked phrase 1]"
- "[Placeholder: locked phrase 2]"
- "[Placeholder: locked phrase 3]"

---

## File Naming Conventions

[Placeholder: naming patterns per asset type. Workers consult this when creating new files so cross-references stay greppable.]

| Asset | Pattern |
| --- | --- |
| Articles | `article-[nn]-[slug].md` |
| Article scripts | `article-[nn]-script.md` |
| Article design briefs | `article-[nn]-design-brief.md` |
| Per-format render scripts | `[format]-[nn].js` |
| Slide decks | `slide-[nn].png` in `slides/article-[nn]/` |
| Thumbnails | `article-[nn]-thumbnail.png` |
| Posts | `[platform]-[topic]-post.md` |
| Reel covers | `[brand]_cover_[topic].png` |

---

## Energy Restorers

For unexpected free time or low-energy days when the planned work isn't viable. These recharge rather than drain. Used by daily-brief generator (Plan B section) and by operator on Low-energy days.

| Activity | Best time | Why it works |
| --- | --- | --- |
| _[Placeholder — operator to fill]_ | _e.g., morning_ | _e.g., outdoor light + movement before any screen_ |

*Operator: replace placeholder rows with what actually restores you. Don't invent — only what you've tested. Update during weekly retrospective if a new restorer surfaces.*

---

## New Article Checklist

When building a new article, these are the deliverables:

[Placeholder: customize per your sandbox set. Example structure for a content + design split:]

Writing team delivers (to `content-claude/articles/`):

- [ ] `article-[nn]-[slug].md` — full article + thread + email broadcast copy
- [ ] `article-[nn]-script.md` — talking-head or podcast script
- [ ] `article-[nn]-design-brief.md` → drop in `design-claude/articles/briefs/`

Design team delivers (to `design-claude/articles/`):

- [ ] 10 slides → `slides/article-[nn]/slide-01.png` through `slide-10.png`
- [ ] Thumbnail → `thumbnails/article-[nn]-thumbnail.png`
- [ ] Story / vertical → `stories/article-[nn]-story.png`
- [ ] One render script: `scripts/article-[nn].js` generates all three in one run
- [ ] Update the per-deliverable tracker (e.g., `CONTENT-STATUS.md`)
