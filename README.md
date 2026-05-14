# Agency of One

A Claude Code template for running a content/design business as a solo operator with one orchestrator and several worker sandboxes. The orchestrator plans and dispatches; workers execute inside their own sandbox; briefs are the handoff contract between them. The template ships the *structure* — folders, brief templates, hooks, skills, routine specs, ICM-aligned context layers — without the operator's actual brand content. You fill in your brand and content; the architecture works on day one.

---

## What this gives you

- **Orchestrator + workers pattern** — one human-in-the-loop session at root, several specialized sandboxes underneath (`content-claude/`, `design-claude/`, `va/`)
- **Briefs as handoffs** — every dispatch is a cold-start brief a worker can read without prior chat history
- **ICM-aligned context layers** — root `CLAUDE.md` (L0), root `CONTEXT.md` (L1), `_config/` + sandbox references (L3), per-brief working artifacts (L4) — see `ARCHITECTURE.md` for the full mapping and why this template skips L2
- **Weekly + monthly maintenance routines** — workers purge, orchestrator audits, operator validates; monthly adds heavier compression and the archive sweep
- **Two skills** — `diagnose-recurring-edits` (aggregate breadcrumbs into source-level fix candidates) and `verify-handoff` (cross-check shipped output against the dispatching brief)
- **Four hooks** — `safety-check.py` (rm -rf / force-push prompt), `snapshot-before-edit.py` (start-of-day snapshots of high-blast-radius files), `auto-stamp-date.py` (auto-bumps `Last updated:` on tracker edits), `handoff-files-guard.py` (prompts before editing handed-off files)
- **Memory pattern** — `MEMORY.md` index + scoped subfolders, with explicit slots for `user`, `feedback`, `project`, and `reference` memories

---

## The architecture in 60 seconds

The orchestrator at the project root reads `STATUS.md` first, then routes via `CONTEXT.md` into whichever sandbox the task lives in. Each sandbox is self-contained: own `CLAUDE.md`, own `CONTEXT.md`, own `STATUS.md`. Workers never read each other's files; they hand off through briefs in the orchestrator's `briefs/` folder, which is the only place dispatches land. Memory loads automatically per the index in `MEMORY.md`. Per-scope `STATUS.md` is the first read at session start and the last write at session end — that's the "did the dispatch land" signal that removes the operator-as-message-bus dependency.

For depth: `ARCHITECTURE.md` (the five-layer ICM mapping, the worker mesh, the maintenance cycles, the diagram).

---

## Install / setup

```bash
git clone <this-repo> ~/Desktop/<your-project>
cd ~/Desktop/<your-project>
```

Then, in three steps:

1. **Run the workspace-builder routine** to populate `_config/BRAND.md` and `_config/REFERENCE.md` with your voice rules, key phrases, banned vocabulary, brand tokens, file-naming conventions. Trigger phrase: *"workspace builder"*. Spec: `briefs/_WORKSPACE-BUILDER.md`.
2. **Write your first calendar.** Trigger: *"build [month] calendar"*. Spec: `briefs/_CALENDAR-TEMPLATE.md`. Shape reference: `EXAMPLE-MONTH-CALENDAR.md`.
3. **Open Claude Code at the project root** and dispatch your first brief. The example in `briefs/EXAMPLE-article-brief.md` shows the full shape; copy it, replace the slug, fill the sections.

The `.claude/settings.json` ships with a minimal allow-list and the four hooks wired in. The hooks fire automatically on the events they're matched to — no per-session configuration.

---

## One example day

Monday, 8am. Operator types *"execute Monday"* in the orchestrator session.

1. **Orchestrator pre-flights.** Greps one row from the active month's calendar (3–5 lines). Checks: does `content-claude/posts/[slug]-post.md` exist? Does `design-claude/final/[brand]_cover_[slug].png` exist? Is the photo source obvious from the row?
2. **Orchestrator writes the dispatch.** Copies the paste-template from `briefs/_PASTE-SNIPPETS.md` (Snippet A for design-claude; Snippet B for content-claude when the caption MD is missing). Fills the seven pre-decided fields: date, calendar row, phrase, slug, category, caption-source, photo-source.
3. **Operator pastes into a fresh design-claude session.** Worker reads the prompt, builds the two reel covers (text-only fallback + photo-driven editorial), refreshes `daily/THIS-WEEK.html`, embeds the caption verbatim from the post MD.
4. **Worker drops a breadcrumb.** One line appended to root `STATUS.md` "Recently shipped": *`2026-05-05 09:14 — design-claude SHIPPED <slug> → design-claude/final/[brand]_cover_<slug>.png, daily/THIS-WEEK.html`*.
5. **Orchestrator runs `/verify-handoff`.** Skill reads the brief's Inputs/Returns-with sections, confirms files exist, checks PNG dimensions match spec, confirms the caption MD substring appears in the dashboard HTML body. Verdict: CLEAN.
6. **Done.** Operator sees the dashboard, posts when ready, marks the per-deliverable tracker live after the post lands.

Routine days run ~5–10k tokens. The full-brief mode (operator says *"full brief"*) is opt-in for ambiguous days only.

---

## File layout

```text
agency-of-one/
├── README.md                       ← this file
├── ARCHITECTURE.md                 ← the five-layer ICM mapping + diagram
├── LICENSE.md                      ← PolyForm Noncommercial 1.0.0
├── CLAUDE.md                       ← orchestrator master control (operator triggers, what-not-to-do)
├── CONTEXT.md                      ← who, what's active, what to load per task
├── STATUS.md                       ← active threads, next moves, recently shipped (workers' breadcrumb target)
├── MEMORY.md                       ← auto-loaded memory index (pointers, not content)
├── EXAMPLE-MONTH-CALENDAR.md       ← shape reference for monthly calendars
├── ideas.md                        ← inbox for stray thoughts, routed by tag
├── .claude/
│   ├── settings.json               ← permissions allow-list + hook wiring
│   ├── hooks/
│   │   ├── auto-stamp-date.py      ← post-edit: bumps "Last updated:" on tracker edits
│   │   ├── safety-check.py         ← pre-Bash: prompts on rm -rf / git push --force
│   │   ├── snapshot-before-edit.py ← pre-Edit: copies high-blast-radius files to .trash/YYYY-MM-DD/
│   │   └── handoff-files-guard.py  ← pre-Edit: prompts before editing handed-off files (operator populates HANDOFF_MARKERS)
│   └── skills/
│       ├── diagnose-recurring-edits/SKILL.md  ← aggregates breadcrumbs into source-fix candidates
│       └── verify-handoff/SKILL.md            ← cross-checks shipped output against brief
├── _config/
│   ├── _WORKER-RULES.md            ← cross-cutting worker rules (sandbox boundary, escalation, breadcrumbs)
│   ├── COMMON-MISTAKES.md          ← anti-patterns with caught-date and fix per entry
│   ├── BRAND.md                    ← voice rules, key phrases, banned vocabulary, design rules
│   ├── REFERENCE.md                ← brand tokens, design specs, file naming, key phrases
│   └── RELATED_PROJECTS.md         ← properties owned by your brand (cross-link rules)
├── briefs/
│   ├── _BRIEF-TEMPLATE.md          ← six-section template — copy, fill slug, dispatch
│   ├── _IG-BRIEF-TEMPLATE.md       ← social-post design brief (carousel / single / cover)
│   ├── _CALENDAR-TEMPLATE.md       ← monthly calendar pattern (lean day-by-day + sibling strategy file)
│   ├── _TODAY-TEMPLATE.md          ← daily dispatch full spec (load on full-brief mode only)
│   ├── _PASTE-SNIPPETS.md          ← canonical paste-templates for routine daily dispatch
│   ├── _WEEKLY-MAINTENANCE.md      ← Sunday weekly sweep (4 phases)
│   ├── _MONTHLY-MAINTENANCE.md     ← first-Sunday-of-month structural compression
│   ├── _ARCHIVE-MONTH.md           ← out-of-tree archive sweep
│   ├── _WORKSPACE-BUILDER.md       ← spin up a new worker sandbox via 9-question questionnaire
│   ├── _IDEAS-PROCESSING.md        ← route tagged bullets from ideas.md
│   ├── _WEEKLY-HTML-TEMPLATE.md    ← rolling weekly dashboard spec (design-claude artifact)
│   ├── _PENDING-ASSETS.md          ← outstanding asset asks awaiting the operator
│   ├── _MONTHLY-AUDIT-LOG.md       ← architectural-additions tracker; first-weekly-of-month audit
│   ├── EXAMPLE-article-brief.md    ← canonical filled example (non-domain-specific)
│   └── questions/                  ← worker escalation files (orchestrator reads next session)
├── sandboxes/
│   ├── content-claude/             ← writing sandbox — articles, podcast, posts, long-form editing
│   │   ├── CLAUDE.md
│   │   ├── CONTEXT.md
│   │   └── STATUS.md
│   ├── design-claude/              ← visual sandbox — covers, illustrations, slide decks, the daily dashboard
│   │   ├── CLAUDE.md
│   │   ├── CONTEXT.md
│   │   └── STATUS.md
│   └── va/                         ← handoff-team sandbox — files prepared for VA / contractor execution
│       ├── CLAUDE.md
│       ├── CONTEXT.md
│       └── STATUS.md
└── daily/
    └── README.md                   ← describes the rolling weekly dashboard pattern (THIS-WEEK.html lives here once design-claude is dispatched)
```

---

## Where this came from

This template is one operator's domain-specific implementation of the **Interpretable Context Methodology** (van Clief & McDermott, *arXiv:2603.16021v2 — "Interpretable Context Methodology: Folder Structure as Agent Architecture"*). The five-layer mapping (L0/L1/L2/L3/L4), the edit-source feedback loop (§ 6.3), the cross-stage trace verification (§ 6.2), the workspace-builder pattern (§ 4.4) — all of those live in the paper. This template is what they look like when stretched across a content-and-design business that ships every day. The shape would be different for a different domain; the underlying pattern is the same.

---

## License

This template is licensed under the **PolyForm Noncommercial License 1.0.0** — free for personal, educational, and other non-commercial use. Commercial use (using this template inside a business that derives revenue from the resulting workflow, or selling derivatives of it) requires a separate license. See `LICENSE.md`.

---

## Built further

This template is the surface layer of a system that's been running in production for over a year. The version we run privately includes brand-specific voice machinery, multi-channel calendar automation, video animation pipelines, book-publishing workflows, and a worker mesh tuned to the specific economics of a solo creator business.

If you're building something serious with Claude Code and want to skip the year of trial-and-error, the operator behind this template is available to design and build a custom version for your domain. Email **khanomhotyoga@gmail.com** with what you're building and what you want it to do. Selective engagements only.
