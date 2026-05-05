# ARCHITECTURE

> How the template fits together. The conceptual spine is **Interpretable Context Methodology** (van Clief & McDermott, *arXiv:2603.16021v2 — "Interpretable Context Methodology: Folder Structure as Agent Architecture"*). This document maps the paper's five-layer model onto the concrete files in this repo, names the design choices that depart from the paper, and shows the maintenance cycles that keep the surface bounded over time.

---

## 1. Overview

The problem this architecture solves: **a solo operator with multi-domain output (content + design + a handoff team) needs one human-in-the-loop and several specialized AI seats.** The naive setup — one Claude session that does everything — drifts within a week. The operator becomes the message bus. Token cost grows linearly with the project. Voice rules drift across domains. Briefs that worked in one session don't work in the next because the context that made them work doesn't survive.

The template's answer is the orchestrator + workers pattern from ICM. One orchestrator session at the project root coordinates and dispatches. Several worker sandboxes execute. Briefs in `briefs/` are the only contract that crosses sandbox boundaries. Memory loads automatically per scope. `STATUS.md` files at each level act as the first-read / last-write surface that absorbs the message-bus duty the operator used to carry.

---

## 2. The five-layer ICM mapping

The ICM paper defines five layers of context (L0 through L4). This template uses **L0 / L1 / L3 / L4 — no L2**.

| Layer | What it is (per ICM) | This template's files |
| --- | --- | --- |
| **L0** | Identity / role / agent-definition | Root `CLAUDE.md` — names the orchestrator role, the operator triggers, the hard "what not to do" rules. Sandbox `CLAUDE.md` files do the same job at worker scope. |
| **L1** | Routing / what's active / where to look | Root `CONTEXT.md` — the task-routing table with Load / Then-load / Skip columns. Sandbox `CONTEXT.md` files do the same job at worker scope. `STATUS.md` (root and sandbox) is also L1: a first-read surface that maps what's active *right now* without loading deeper context. |
| **L2** | (Stage-specific reference, always loaded for the active stage) | **This template skips L2.** See § "Why no L2" below. |
| **L3** | Reference / factory / always-loaded shared rules | `_config/` — `BRAND.md` (voice + design), `REFERENCE.md` (tokens + naming), `_WORKER-RULES.md` (cross-cutting), `COMMON-MISTAKES.md` (anti-patterns). Sandbox-local references (e.g., a `BOOK-LAYOUT-Reference.md` that only design-claude reads) are L3 within the sandbox. |
| **L4** | Working artifacts / per-task material | `briefs/<slug>.md` (the handoff contract). The brief's Inputs table names every other L4 file the worker reads — drafts, post copy, photo paths, prior-stage output. The brief is the only authorization that lets a worker open an L4 file. |

### Why no L2

ICM uses L2 for stage-specific reference material that's always loaded once a stage is active — e.g., "you're in the writing stage; here are the writing-stage rules." That works for systems where stages are coarse and rules-per-stage are small. In a daily content/design loop, every dispatch has its own stage, and pre-loading stage rules per dispatch grows the always-loaded surface fast.

This template collapses L2 into per-brief Inputs tables. Each brief names exactly the files it needs from L3 (factory) and L4 (working artifacts) — no implicit "stage rules" load. The cost is that the brief author has to be specific about Inputs (which is good discipline anyway). The benefit is that always-loaded surface stays bounded: only L0 (CLAUDE.md), L1 (CONTEXT.md, STATUS.md), and a small slice of L3 (the entries the brief explicitly names) cost tokens at session start.

This is documented as a deliberate departure from the paper, not an oversight. If your domain has cleanly-separable stages with stable per-stage rules, you can re-introduce L2 by adding a stage-rules file under each sandbox and pointing the dispatch prompt at it. Most creator domains don't need it.

### Sandbox CLAUDE.md as L1, not a second L0

Each sandbox `CLAUDE.md` acts as a routing surface for its own scope. A worker reads it and learns which file to open next — that's L1 behavior, not L0. The L0 role for the worker is implicit (it's a content-claude session, or a design-claude session — the role is the sandbox name). This matters when you go to expand the architecture: don't write biographical rules into a sandbox CLAUDE.md ("you are a writing assistant that…"), because that's L0 noise the worker already has from being in the sandbox.

---

## 3. Orchestrator + workers model

One orchestrator. Three worker sandboxes ship with the template:

- **content-claude** — writes prose. Articles, podcast scripts, social posts, email sequences, ad copy. Output type: `.md` files in the appropriate subfolder.
- **design-claude** — produces visuals. Covers, illustrations, slide decks, thumbnails, the rolling weekly dashboard. Output type: `.png` and one rolling `.html`.
- **va** (or `handoff-team`) — drafts the handoff packs that downstream humans (VA / contractor / freelancer) execute against. Output type: `.html` build briefs, `.md` checklists, asset folders.

Add more sandboxes via the workspace-builder routine (`briefs/_WORKSPACE-BUILDER.md`) — a 9-question questionnaire that produces a clean sandbox plus the cross-cutting registry updates. Common additions: `fb-ads-claude`, `coaching-claude`, an animation worker, a transcription worker.

### Briefs as handoff contracts

Every dispatch is a brief. Briefs follow the six-section template in `briefs/_BRIEF-TEMPLATE.md`:

1. **Task** — the outcome in one paragraph
2. **Inputs** — every L3 + L4 file the worker reads, with section pointers
3. **Scope** — in-scope, out-of-scope, kill-switch
4. **Acceptance** — binary checks (file exists, tracker updated, etc.)
5. **Verify** — cross-stage checks the worker runs before returning
6. **Returns-with** — the deliverable list the worker produces

The cold-start rule (`CONTEXT.md`): if the brief can't stand alone without this chat history, it isn't finished. A brief tested cold once survives any future session.

### The sandbox-boundary hard rule

`_config/_WORKER-RULES.md § 1` is the only rule with no exceptions: **workers never modify files outside their sandbox.** The brief's Returns-with section is the only authorization that crosses the boundary (e.g., design-claude is allowed to write `daily/THIS-WEEK.html` because that path is named in its dispatch).

A worker that "fixes" something outside its sandbox creates cross-sandbox drift that's expensive to diagnose later. The rule trades off small short-term inconvenience (the worker has to flag and stop) for the durability that lets sessions stay coherent over weeks.

---

## 4. Memory model

Memory is auto-loaded by Claude Code per the index in `MEMORY.md`. The index points to scoped subfolders under `~/.claude/projects/-<flattened-project-path>/memory/`:

- **`_global/`** — facts that apply across all sandboxes. Loaded at every session.
- **`orchestrator/`** — initiatives the orchestrator is steering, in-flight project state, recent retrospectives. Loaded when the orchestrator session starts.
- **per-worker folders** (`content-claude/`, `design-claude/`, `va/`, etc.) — feedback the worker should remember. Loaded only when that worker's session starts inside its sandbox.

### Four types of memory

| Type | What it is | When to write |
| --- | --- | --- |
| **user** | Operator's role, preferences, knowledge | When the operator names a fact about themselves |
| **feedback** | Corrections + validated approaches | When the operator corrects you OR validates a non-obvious choice |
| **project** | In-flight initiatives, deadlines, decisions | When you learn who's doing what, why, by when |
| **reference** | Pointers to external systems | When you learn where to look (Linear project, Slack channel, dashboard URL) |

### What NOT to put in memory

Patterns derivable from the codebase (folder structure, file paths, conventions). Git history. Debugging recipes. Anything documented in `CLAUDE.md` files. Ephemeral task state that belongs in `STATUS.md` or a brief.

The bias is to under-write memory rather than over-write. Memories that go stale corrupt sessions; missing memories cost a few tokens to re-derive.

---

## 5. Maintenance routines

Two cycles keep the architecture from drifting.

### Weekly maintenance (Sundays)

Spec: `briefs/_WEEKLY-MAINTENANCE.md`. Four phases:

1. **Worker purge dispatch** (parallel) — each worker archives completed briefs, moves stale drafts, flags patterns.
2. **Orchestrator structural sweep** (single session) — invokes `/diagnose-recurring-edits`, audits memory, audits `_config/`, resolves `briefs/questions/`, reconciles the per-deliverable tracker, pre-flights next week's calendar, audits registries, processes the ideas inbox count, writes the weekly retrospective, measures token-surface and scan-surface drift, prunes `.trash/` snapshots.
3. **Operator validation gate** — operator approves / edits / rejects each proposed structural change. Rejections logged.
4. **Optional: workspace-builder** — if a new worker is being added this week, run it after maintenance lands.

### Monthly maintenance (first Sunday of month)

Spec: `briefs/_MONTHLY-MAINTENANCE.md`. Heavier compression, runs after the weekly that day:

1. **Auto-trigger `archive [month]`** for the prior calendar month — source files for posted prior-month items move to the configured external archive folder. Rendered outputs stay.
2. **Monthly audit log update** — the architectural-additions tracker in `briefs/_MONTHLY-AUDIT-LOG.md` gets a new row; retire/adapt candidates surface for operator decision.
3. **Always-loaded surface compression** — files flagged in last week's measurement step get compressed proposals (no auto-apply).
4. **Deeper `_config/` audit** — full read of BRAND.md, REFERENCE.md, RELATED_PROJECTS.md, _WORKER-RULES.md, COMMON-MISTAKES.md.
5. **Cross-sandbox registry consistency** — root CLAUDE.md SANDBOXES table, root CONTEXT.md task-routing rows, MEMORY.md scopes, RELATED_PROJECTS — all must agree with each other and with reality on disk.
6. **Next month's calendar build** — if not yet built.
7. **Operator validation gate** — same shape as weekly Phase 3.

The cadence is intentional: weekly handles flags and small drift; monthly handles structural compression. Doing structural work weekly burns operator attention; doing it less than monthly lets cruft accumulate.

---

## 6. Hooks + skills

### Hooks (`.claude/hooks/`)

Four hooks ship wired into `.claude/settings.json`. They fire automatically; the operator doesn't invoke them.

| Hook | When it fires | What it does |
| --- | --- | --- |
| `safety-check.py` | Pre-Bash | Detects `rm -rf` (any flag combination) and `git push --force` / `-f`. Forces an "ask" prompt — even in `bypassPermissions` mode. Everything else passes through. |
| `snapshot-before-edit.py` | Pre-Edit / Pre-Write / Pre-MultiEdit | On the first edit per day to a high-blast-radius file (root control files, `_config/*`, `.claude/settings.json`, sandbox CLAUDE/STATUS/CONTEXT, `briefs/_*.md`), copies the original to `.trash/YYYY-MM-DD/<flattened-path>`. Acts as a "git revert without git" floor. PROJECT_ROOT resolves dynamically (`$CLAUDE_PROJECT_DIR` or walk-up from hook location) so the same hook works in any clone. |
| `auto-stamp-date.py` | Post-Edit / Post-Write / Post-MultiEdit | When a file ending in `CONTENT-STATUS.md` is edited, bumps the `Last updated:` line at the top of the file to today's date. Saves one Edit call per content update. |
| `handoff-files-guard.py` | Pre-Edit / Pre-Write / Pre-MultiEdit | When the edited path contains any of the substrings in `HANDOFF_MARKERS` (operator-populated), prompts before letting the edit land. Operator's defense against accidentally editing files a downstream human is executing against. |

### Skills (`.claude/skills/`)

| Skill | When to invoke | What it does |
| --- | --- | --- |
| `/diagnose-recurring-edits` | Weekly maintenance Phase 2 step 1; after a `-redo` dispatch; operator asks "what keeps breaking" | Aggregates breadcrumbs from all sandbox `STATUS.md` "Recently shipped" sections + escalations in `briefs/questions/` over the last 14–30 days. Surfaces patterns (3+ same-shape corrections, repeated self-flags, missing-field escalations, recurring questions) with source-level fix candidates. Implements ICM § 6.3 edit-source loop. Does not modify files. |
| `/verify-handoff` | After a worker breadcrumb lands; before declaring a session shipped; operator asks "verify [slug]" / "did [worker] do it right" | Cross-checks shipped output against the dispatching brief's Inputs / Returns-with / Verify sections. Always-checks: file exists, mtime within window, inputs all readable, slug consistency. Format-specific: PNG dimensions match spec; HTML body contains caption substring (catches the "file exists but content wrong" defect class); MD non-empty + has expected blocks. Implements ICM § 6.2 cross-stage trace verification. Does not modify files. |

---

## 7. Diagram

```text
                              OPERATOR
                                 │
                                 ▼
                ┌──────────────────────────────────┐
                │   ORCHESTRATOR  (project root)   │  L0: CLAUDE.md
                │                                  │  L1: CONTEXT.md, STATUS.md
                │   - operator triggers            │  L3: _config/*, briefs/_*.md
                │   - dispatches via briefs/       │  L4: briefs/<slug>.md
                │   - reads STATUS.md first        │
                └────────┬───────────┬─────────────┘
                         │           │
              ┌──────────┘           └──────────┐
              ▼                                 ▼
       ┌──────────────┐                  ┌──────────────┐
       │ briefs/      │ ← only contract  │ MEMORY.md    │ ← auto-loaded
       │ <slug>.md    │   that crosses   │ ─ _global/   │   index
       │              │   the boundary   │ ─ orch/      │
       └──┬─────┬──┬──┘                  │ ─ <worker>/  │
          │     │  │                     └──────────────┘
          │     │  │
   ┌──────▼─┐ ┌─▼┐ │
   │content-│ │de│ │     L0/L1: sandbox CLAUDE.md, CONTEXT.md, STATUS.md
   │claude/ │ │si│ │     L3:    sandbox-local references (e.g. BOOK-LAYOUT)
   │        │ │gn│ │     L4:    per-brief working files (Inputs table)
   │ posts/ │ │- │ │
   │ articl │ │cl│ │     Workers:
   │ podcast│ │au│ │      ─ never modify files outside their sandbox
   │        │ │de│ │      ─ append breadcrumb to root STATUS.md as final action
   └────────┘ └──┘ │      ─ escalate to briefs/questions/<slug>-question.md
                   │
                ┌──▼──┐
                │ va/ │  handoff-ready files for downstream human
                │     │  no-edit-after-handoff hard rule
                └─────┘

   .claude/hooks/ fire automatically:
     safety-check         → pre-Bash (rm -rf / push --force)
     snapshot-before-edit → pre-Edit (high-blast-radius files → .trash/YYYY-MM-DD/)
     auto-stamp-date      → post-Edit (CONTENT-STATUS.md "Last updated:" bump)
     handoff-files-guard  → pre-Edit (handoff-marker paths → prompt)

   .claude/skills/ run on demand:
     /diagnose-recurring-edits → ICM § 6.3 edit-source loop
     /verify-handoff           → ICM § 6.2 cross-stage trace verification

   Maintenance cycles:
     weekly  (Sundays)         → workers purge → orchestrator audits → operator validates
     monthly (first Sunday)    → archive prior month + always-loaded compression + registry consistency
```

---

## Folder layout choice

The template ships sandboxes under `sandboxes/` (the public-template choice) rather than at root (the original HQ pattern). The trade-off:

- **`sandboxes/<worker>/`** (this template's default) — keeps the project root tidy. Workers cd into `sandboxes/content-claude/`. Cross-sandbox paths from a worker are `../../_config/...` and `../../daily/...` — one extra `../`.
- **`<worker>/` at root** — flat structure, paths are one segment shorter. Project root has more top-level folders.

Both work. Pick one and keep it consistent — the path conventions baked into briefs and CLAUDE.md files assume the choice. If you move sandboxes between layouts, run a project-wide grep for `../` paths and fix them in one pass.
