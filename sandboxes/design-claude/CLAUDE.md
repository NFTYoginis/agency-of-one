# design-claude

Visual and design sandbox. All image outputs, PNGs, covers, illustrations, slide decks, and the rolling weekly dashboard live here. Written content (podcast, article, post copy) → `../content-claude/`.

Check [STATUS.md](STATUS.md) first — if the request is a small follow-up already mapped there, you may not need anything else. Otherwise: read `CONTEXT.md` for current design priorities and task loading, then `../_config/REFERENCE.md` for brand colors, design specs, naming conventions, and the article checklist.

Update STATUS.md at end of any session that ships an asset, dispatches a brief, or shifts a thread (per `../_config/_WORKER-RULES.md` § 10).

---

## Cross-cutting worker rules

Read `../_config/_WORKER-RULES.md` before any file operation. Sandbox boundary, memory rules, status tracking, voice rules, escalation — single source of truth shared across all workers.

---

## Folder Structure

```text
design-claude/
├── CLAUDE.md                  ← this file — Map + technical execution specs
├── CONTEXT.md                 ← current priorities, task loading
├── STATUS.md                  ← active threads, next moves, recently shipped
├── articles/
│   ├── briefs/                ← article-[nn]-design-brief.md (from writing team — read first)
│   ├── slides/                ← slide deck PNGs per article
│   ├── thumbnails/            ← thumbnail PNGs
│   └── stories/               ← vertical story PNGs
├── illustrations/             ← labeled-figure PNGs (cards / diagrams)
│   └── briefs/                ← DESIGN-*.md specs + visual references
├── posts/
│   ├── covers/                ← reel cover PNGs + source files
│   └── carousel/              ← carousel slide PNGs
├── Book Cover/                ← book / long-form cover outputs per title
├── drafts/                    ← work-in-progress
├── final/                     ← approved final outputs
├── scripts/                   ← Node.js generation scripts
└── briefs/                    ← briefs received from orchestrator
```

> Adapt subfolders to your own output set. The shape above is a starting point.

---

## Article Production Workflow

Writing team drops a brief into `articles/briefs/`. Always read that brief before starting.

One script per article: `scripts/article-[nn].js` generates all deliverables in one command.

```bash
node scripts/article-NN.js
```

Outputs:

| Deliverable | Destination |
| --- | --- |
| 10 slide PNGs | `articles/slides/article-[nn]/slide-01.png` through `slide-10.png` |
| Thumbnail | `articles/thumbnails/article-[nn]-thumbnail.png` |
| Story / vertical | `articles/stories/article-[nn]-story.png` |

Use the first article's script as the template — copy it, update the data. Scripts get organized in category subfolders as the project grows (`articles/`, `book-covers/`, `daily/`, etc.) — see `scripts/README.md` for the map. New render scripts go directly into the matching subfolder, not at scripts/ root.

---

## Cover Policy — Visuals Required

Every cover post gets a visual. Text-only is fallback only — `generate_cover.js` is the last-resort generator.

**Decision flow per cover:**
1. Read the post topic / context
2. Pick CREATE or CURATE:
   - **Create** when topic suggests a specific scene, figure, or diagram → use your image-gen pipeline (photo backgrounds + composed typography, or illustrated figures + labeled diagrams)
   - **Curate** when a relevant existing photo lives in the photo library
3. Compose typography on top via `html-to-image` or Puppeteer
4. Brand rules still hold: see `../_config/BRAND.md` § 6

---

## Image Generation — Text-Only Reel Covers (fallback)

Stack: Node.js + `sharp` + embedded SVG + brand font (base64 encoded so Puppeteer/Canvas don't fall back to system fonts)
Output: brand spec size → `drafts/[brand]_cover_[topic].png`
Safe zone: 15% inset all edges — exact x/y per `../_config/REFERENCE.md` Design Specs

Fixed layout — never move elements. The element-position table lives in `../_config/REFERENCE.md` once you've locked your cover layout. Workers reference that table; this CLAUDE.md just notes that the layout is locked, not where each element sits.

---

## Image Generation — Labeled Illustrations / Diagrams (Puppeteer → PNG)

Stack: HTML + SVG cards → Puppeteer headless Chrome → PNG
Chrome path: configure per-machine in your render script
Output size: per `../_config/REFERENCE.md` Design Specs (illustrations row)
Settle time: 2000ms before screenshotting

Card CSS structure: `.series-tag` · `.title` · `.sub` · `.rule` · `.figure-wrap` (SVG) · `.legend` · `.footer`
Naming: per `../_config/REFERENCE.md` "File Naming Conventions"
Brief files: `illustrations/briefs/DESIGN-[topic]-Illustration-Brief.md`

**Save the render script alongside the PNG.** See `../_config/COMMON-MISTAKES.md` § 0 — ephemeral generation is the most expensive failure mode in this sandbox.

---

## Photo-Backed Slides, Thumbnails, Stories

Stack: AI photo via your image-generation MCP + text overlay via `html-to-image`

Background direction: high-key, well-lit photos — outdoor light, natural settings, warm daylight. (Adjust per `../_config/BRAND.md` § 7.)
Overlay opacity: max per `../_config/REFERENCE.md` (typically `0.40`). Most slides: `0.25–0.38`. Never go dark to compensate for a weak photo — choose a better photo.
Vary overlay tone intentionally across a slide deck — not all dark, not all light.

---

## Output Rules

- Reel covers → `drafts/` until approved, then `final/`
- Illustrations → `illustrations/` (permanent — never overwrite without intent)
- Platform assets → their own folder
- Book / long-form covers → `Book Cover/[Title]/`
- Update the per-deliverable tracker (project root) after completing any asset
