# 2026-05-deep-work-scheduling-for-solo-operators

**Worker:** content-claude
**Sandbox:** `sandboxes/content-claude/CLAUDE.md`
**Date:** 2026-05-05

---

## Orchestrator pre-draft check

- [x] In scope for the May productivity-newsletter sprint
- [x] Single stage (research already complete in prior dispatch)
- [x] Source files ready (interview transcripts + reader-survey results in `content-claude/research/`)
- [x] Brief is under 200 lines

---

## Task

Produce the full deliverable set for the May feature article on *Deep work scheduling for solo operators* — the written article with X thread and email broadcast, the talking-head script for the YouTube companion, and the design brief that drives the slide deck + thumbnail + story. The article translates the operator-survey finding ("solo operators block deep-work time but break it themselves within 90 minutes") into an actionable scheduling pattern. Tone: peer-to-peer, direct, no productivity hype.

---

## Inputs

| Layer | File | Why it matters | Sections to focus on |
| --- | --- | --- | --- |
| 3 (reference) | `_config/BRAND.md` | voice rules, banned vocabulary, the peer-to-peer register | §3 voice rules, §4 key phrases |
| 3 (reference) | `_config/REFERENCE.md` | file naming, locked phrases | "File Naming Conventions", "Key Phrases" |
| 4 (working) | `content-claude/research/2026-04-reader-survey-summary.md` | survey finding that drives the article | top 3 patterns from §2 |
| 4 (working) | `content-claude/research/interviews/2026-04-interview-transcripts/` | source quotes from operators | first 60 min of each transcript |
| 4 (working) | `content-claude/articles/article-04-defragmenting-your-week.md` | prior article in the series — tone reference | full read for register match |

Workers must NOT load files that aren't in this table. If a file seems missing, escalate — do not load speculatively.

---

## Scope

**In-scope:**
- `content-claude/articles/article-05-deep-work-scheduling-for-solo-operators.md`
- `content-claude/articles/article-05-script.md` (7–9 min talking-head format)
- `design-claude/articles/briefs/article-05-design-brief.md`

**Out-of-scope:**
- Do not touch any article 01–04 files
- Do not generate slides, thumbnails, or stories — design worker handles those from the brief
- Do not post or schedule anything
- Do not run the operator-survey data through any tool — the summary is the input; the raw data is not

**Kill-switch:** If the article 05 slot in the content-team guide is ambiguous or contradicted by existing files, escalate before writing.

---

## Acceptance

- [ ] `content-claude/articles/article-05-deep-work-scheduling-for-solo-operators.md` exists and contains: full article (1500–1800 words), X thread (7–10 posts, single-line each), email broadcast (300–500 words, distinct hook from the article opening)
- [ ] `content-claude/articles/article-05-script.md` exists, 7–9 min talking-head format with timed sections
- [ ] `design-claude/articles/briefs/article-05-design-brief.md` exists with: tagline, 10-slide deck (copy + visual direction per slide), story copy, thumbnail concept
- [ ] No banned-vocabulary terms (per `_config/BRAND.md` § 3) in any of the three files
- [ ] At least one verbatim Key Phrase from `_config/REFERENCE.md` lands in the article body
- [ ] Per-deliverable tracker has a new row for article 05 marked Ready

---

## Verify

- [ ] Output passes `_config/BRAND.md` voice rules: zero emojis, em-dash count ≤1 per page, no AI-business-speak (leverage / streamline / empower / cutting-edge / seamless / robust solution / delve into / navigate)
- [ ] Every survey statistic cited matches the survey summary file exactly — no rounded numbers, no inferred percentages
- [ ] Every operator quote attributed to a transcript file by line range (`interview-03.md:42-58`)
- [ ] No invented file paths in the design brief — every asset path it references resolves to a real file in `design-claude/` or to a `[Placeholder:]` block
- [ ] No URLs added beyond the one in the brand reference table — affiliate / referral links would need explicit operator authorization
- [ ] X thread reads as a thread, not as a chopped article — each post is a self-contained beat
- [ ] Email broadcast does NOT recycle the article opening — distinct hook is required (per the project's deliverable convention)

If any verify check fails, fix it before returning.

---

## Escalation

If ambiguity hits at any point — the survey summary contradicts itself, the article-04 register doesn't translate to article-05's topic, the operator's research notes name a fact you can't verify — write the question to:

`briefs/questions/2026-05-deep-work-scheduling-question.md`

Then stop. Do not guess. Do not expand scope. The orchestrator reads it next session.

---

## Returns-with

- [ ] `content-claude/articles/article-05-deep-work-scheduling-for-solo-operators.md`
- [ ] `content-claude/articles/article-05-script.md`
- [ ] `design-claude/articles/briefs/article-05-design-brief.md`
- [ ] Per-deliverable tracker updated with article 05 row marked as Ready
- [ ] One-line breadcrumb appended to root `STATUS.md` "Recently shipped" per `_config/_WORKER-RULES.md` § 11

---

> **Why this is the canonical example:** every section is filled. No `[Placeholder:]` blocks remain. A worker reading this brief cold — no chat history, no prior session — has everything: the outcome, the inputs, the constraints, the binary acceptance criteria, the cross-stage verify checks, the escalation path, and the exact deliverables. That's the cold-start rule from `CONTEXT.md`: if the brief can't stand alone, it isn't finished.
