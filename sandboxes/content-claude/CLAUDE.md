# content-claude

Written content sandbox. Articles, podcasts, social posts, long-form editing, email sequences, ad copy. Visual outputs (PNGs, covers, slide decks) → `../design-claude/`.

Check [STATUS.md](STATUS.md) first — if the request is a small follow-up already mapped there, you may not need anything else. Otherwise: read `CONTEXT.md` for writing environment and task loading, then `../_config/REFERENCE.md` for brand phrases, naming conventions, and the article production checklist.

Update STATUS.md at end of any session that ships a draft, dispatches a brief, or shifts a thread (per `../_config/_WORKER-RULES.md` § 10).

---

## Cross-cutting worker rules

Read `../_config/_WORKER-RULES.md` before any file operation. It defines the sandbox boundary (never modify files outside `content-claude/` without explicit brief authorization), memory-writing rules, status-tracking rules, voice rules, and escalation. Shared across all workers — single source of truth.

---

## Folder Structure

```text
content-claude/
├── CLAUDE.md                 ← this file — Map
├── CONTEXT.md                ← writing environment, task loading, current priorities
├── STATUS.md                 ← active threads, next moves, recently shipped
├── articles/
│   ├── briefs/               ← article-[nn]-[slug]-brief.md before writing
│   └── article-[nn]-[slug].md  ← full article + thread + email broadcast
├── podcast/
│   ├── briefs/               ← podcast-brief-[nn].md
│   └── drafts/               ← podcast-episode-[nn]-draft.md
├── posts/                    ← short-form: [platform]-[topic]-post.md
└── briefs/                   ← briefs received from orchestrator
```

> Adapt the subfolders to your own output set. The shape above is a starting point — the operator's actual folder list lives in this file once filled in.

---

## Content Rules by Folder

### podcast/

[Placeholder: format spec — e.g. "Hook → Problem → Teaching → Example → Takeaway. Length: 35–45 min solo. Tone: structured, deep, peer-to-peer."]
Output: `.md` — brief in `briefs/`, draft in `drafts/`
Naming: `podcast-brief-[nn].md` · `podcast-episode-[nn]-draft.md`

### posts/

Short-form. Educational, direct, no clickbait. One strong idea per post.
Output: `.md` in `posts/`. Naming: `[platform]-[topic]-post.md`

**On post (workflow rule):** when a post ships to platform, move its source MD from `posts/` to `posts/done/`. Don't delete — `done/` is the holding area for shipped sources until monthly archive moves them out of the project folder entirely. Same pattern applies to scripts, podcast drafts, articles: `<folder>/done/` is the standard "shipped, awaiting archive" subfolder convention.

**On creation (per-deliverable tracker coverage):** when a new MD is created (in any source folder), add a row to the per-deliverable tracker immediately with status "Draft" / "Ready" — don't wait until post-time. This keeps weekly maintenance audits able to cross-reference reliably.

---

## Article Production — Handoff Workflow

For each article the writing team produces three files:

| File | Destination |
| --- | --- |
| `article-[nn]-[slug].md` | `articles/` — full article + thread + email broadcast |
| `article-[nn]-script.md` | `articles/` — talking-head or podcast-form script |
| `article-[nn]-design-brief.md` | Drop into `../design-claude/articles/briefs/` — this is the handoff to design |

The design brief contains: tagline · 10-slide deck (copy + visual direction per slide) · vertical / story copy · thumbnail concept.

Design team then runs `node scripts/article-[nn].js` (or its equivalent) → generates all three design deliverables in one command.

---

## Output Rules

- All written work saved as `.md` files in the correct subfolder
- Never generate images here — all visual work belongs in `../design-claude/`
- Update the per-deliverable tracker (project root) whenever a piece is completed or posted
