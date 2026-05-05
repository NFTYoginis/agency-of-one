# _WORKER-RULES.md — Cross-cutting rules every worker reads

> Shared rules that apply to every worker (content-claude, design-claude, handoff-team, plus any future workers spun up via the workspace-builder routine). Loaded by each sandbox's `CLAUDE.md`. Single source of truth — maintenance happens here, not in N sandbox files.

---

## 0. External archive folder is off-limits to workers (hard rule)

**Workers must never scan, list, read from, or write to the external archive folder** — typically a sibling location outside this repo (e.g., `~/Desktop/<project>-Archive/`). Configure the path once in your operator notes; do not hard-code it in worker briefs.

That folder holds prior-month source files that have been archived out of active sandboxes. The whole point of the outside-tree archive is that it costs zero tokens during normal sessions — workers only see active surfaces. If you find yourself wanting to grep, list, or read inside the archive, stop and escalate to the operator.

This rule applies to: `Read`, `Bash` (`ls`/`find`/`grep`/`cat`/`head`/`tail`), `Edit`, `Write`, and any tool that touches the filesystem.

**Access matrix:**

| Actor | Read archive | Write archive |
| --- | --- | --- |
| Workers | Never | Never |
| Orchestrator | Only on explicit operator dispatch naming an archive path | Write-only during scheduled archive routines (`_ARCHIVE-MONTH.md`, `_MONTHLY-MAINTENANCE.md` Phase 1) |
| Operator | Full access | Full access |

The orchestrator's write access exists solely to execute archive moves during scheduled routines. The orchestrator does NOT browse or read from the archive in normal operations — same scan-cost rule applies.

---

## 1. Sandbox boundary (hard rule)

**Never delete or modify any file outside your sandbox folder.** This includes — without exception:

- Root files: `CLAUDE.md`, `CONTEXT.md`, `STATUS.md`, the active calendar (`EXAMPLE-MONTH-CALENDAR.md` template; live calendars follow the same shape)
- The `_config/` folder and everything inside it (`BRAND.md`, `REFERENCE.md`, `RELATED_PROJECTS.md`, this file, etc.)
- The `briefs/` folder (only orchestrator writes here)
- The `daily/` folder (orchestrator writes MD when in opt-in full-brief mode; design-claude writes HTML only when explicitly brief-authorized)
- Any other sandbox folder (`content-claude/`, `design-claude/`, `va/` or `handoff-team/`, plus any custom sandboxes you've added)

**Reading these files is fine** when a brief's Inputs table requires it. **Writing, deleting, or renaming them is not.**

If you encounter a file outside your sandbox that seems wrong, stale, or in conflict with your current task: **flag it in your session output and stop on that point.** The orchestrator decides whether to change it. A worker that silently fixes things outside its sandbox creates cross-sandbox drift that's expensive to diagnose later.

**Exception:** if a brief's Returns-with section explicitly names a file outside your sandbox as a deliverable (e.g., design-claude's rolling weekly dashboard at `daily/THIS-WEEK.html`, or article-design handoff briefs landing in another sandbox's `briefs/` folder), that brief is the authorization. The brief is the only authorization that crosses the boundary.

**Path convention for cross-sandbox reads:** workers' working directory is their sandbox, not the project root. When a brief references project-level files (`_config/`, `briefs/`, `daily/`, etc.), prefix with `../` from inside the sandbox. Bare paths break. The orchestrator's dispatch prompts are written with `../` prefixes already — paste them as given.

---

## 2. Memory writing

Workers do not write directly to `MEMORY.md` or any file in the operator's auto-memory folder. If you notice something worth remembering across sessions, surface it in your session output and the orchestrator decides whether to memorialize it and at what scope (`_global/` vs your worker scope).

---

## 3. Status tracking

The per-deliverable tracker (whatever the operator chose to call it — typical: `CONTENT-STATUS.md` at root) updates only after the operator confirms a piece is live. Workers do not update it from a draft state. If your output is one of the items tracked there, leave the update to the orchestrator.

---

## 4. Voice + brand

Voice rules and brand-token references live in `_config/BRAND.md` and `_config/REFERENCE.md`. Read those when a brief's Inputs table tells you to. Do not paraphrase, "improve," or merge them into worker-specific rules. They are Layer 3 (factory) — internalize as constraints, do not edit.

---

## 5. Escalation

If a brief is missing information, ambiguous, or requests something that conflicts with rules above: **stop and write to `briefs/questions/<slug>-question.md`** as your brief specifies. Do not guess. Do not expand scope to "fix" the ambiguity yourself.

---

## 6. No apologies — fix it

Do not pad responses with *"I apologize for the confusion,"* *"sorry about that,"* or similar. State what went wrong, deliver the fix, move on. Apologies waste tokens and don't change the outcome.

If you delivered something wrong, the right response is one sentence naming the issue + the corrected output. Not three sentences of contrition.

---

## 7. Skill activation — when to invoke built-in skills

Skills are not optional decorations. They are wired into specific workflow moments. If your worker produces user-facing prose, the rules below apply. If you are a design-only worker, skip this section.

| Skill | Triggered by | When to run | How |
| --- | --- | --- | --- |
| `/humanizer` | any worker producing user-facing prose | **Non-negotiable before any draft moves to `final/`** — captions, scripts, articles, email sequences, ad copy, landing copy. | Run on the full draft. Apply suggestions. Re-check `_config/BRAND.md` voice rules + `_config/REFERENCE.md` Key Phrases compliance after the humanizer pass. |
| `/web-design-guidelines` | design workers (web/HTML deliverables only) | Before any HTML/CSS deliverable is moved to a `final/` folder or `daily/THIS-WEEK.html` is committed | Run on the rendered output. Fix accessibility / visual-hierarchy issues. |

**Why this is in `_WORKER-RULES.md` and not each sandbox CLAUDE.md:** the rule is cross-cutting. If the same humanizer pass needs to run on *any* prose deliverable from *any* worker, putting it here keeps a single source of truth. New workers spun up via `_WORKSPACE-BUILDER.md` inherit this rule automatically.

---

## 8. Three-strike rule — escalate, don't iterate

If a worker has rewritten the same output three times based on operator feedback and it's still wrong, the brief is wrong, not the worker. Stop iterating. Escalate via `briefs/questions/<slug>-question.md` with: what you tried (versions 1, 2, 3), what the operator wanted, what you think the gap is, and 2–3 paths forward.

Three identical-shape rewrites means the source needs editing, not the output. Per ICM edit-source principle (paper §6.3): patching the binary doesn't improve the compiler.

---

## 9. Artifact ownership — daily flow boundary (hard rule)

In the default daily flow, each role produces a specific artifact type. Crossing the boundary creates duplicate work.

| Role | Owns | Examples |
| --- | --- | --- |
| **Orchestrator** | Plans + dispatches | Briefs, full-brief daily MDs (opt-in only), dispatch prompts to workers |
| **content-claude** | Prose source files | Post MDs, article drafts, podcast scripts, email sequences, ad copy |
| **design-claude** | Rendered visuals + the dashboard | Cover PNGs, slide PNGs, thumbnails, illustrations, `../daily/THIS-WEEK.html` |

**On the default daily flow, content-claude has no role unless its source MD is missing.** Captions are pulled verbatim by design-claude from existing source MDs. If a caption source doesn't exist, the orchestrator either dispatches content-claude *separately* to write one (parallel-dispatch with design-claude), or sets `caption: operator-live` in the dispatch (caption-less formats only).

**Architecture decision: HTML-only daily flow by default.** No per-day daily MDs in the routine flow. The dashboard's source links go to the calendar row or to source content MDs — never to a `daily/YYYY-MM-DD.md` file, since those only exist in opt-in full-brief mode.

**Exception:** when the operator explicitly cross-dispatches (e.g., *"content-claude, write tomorrow's caption first"*), that's an explicit boundary cross authorized by the operator. The rule above governs the default flow only.

---

## 10. STATUS.md is your first read, your last write

Every sandbox (and the orchestrator root) has a `STATUS.md` co-located with its `CLAUDE.md`. It is the *"where are we / what's next"* one-glance file.

**On session start:** check `STATUS.md` first. If the operator's request is a small follow-up already mapped under Active Threads or Next Moves, you can act without loading CLAUDE.md / CONTEXT.md / brief files. This is the largest token saver in the orchestrator+workers loop — a 50-line read instead of a 600-line tour.

**On session end:** update `STATUS.md` if you shipped a deliverable, dispatched a brief, hit a new blocker, or shifted a thread. Keep it under 60 lines. Sections to maintain in this order:

1. **Active threads** — what's open right now (one line each)
2. **Next moves** — top 3, in execution order
3. **Blocked on operator** — what's waiting on the operator (or pointer to `briefs/_PENDING-ASSETS.md`)
4. **Recently shipped (last 7 days)** — dated bullets; older entries graduate out

When you complete something tracked under Active Threads or Next Moves, move it to Recently Shipped *in the same edit*. Don't leave stale lines.

**The "Last updated:" stamp at the top of STATUS.md must always match the date of your last edit.** This is the trust signal that says "yes, this is current — believe it."

**STATUS.md is not your per-deliverable tracker.** STATUS.md is the orchestrator-or-worker overview (active threads + next moves + blockers, kept tiny). The per-deliverable tracker (e.g., a root `CONTENT-STATUS.md`) is one row per article / post / cover, all detail. Two files, two roles. Don't merge them.

**Workers can write to their own sandbox's STATUS.md only.** Cross-sandbox STATUS.md updates go through the orchestrator (per § 1 sandbox boundary). **Exception:** the dispatch breadcrumb in § 11 — one line to root `STATUS.md`'s "Recently shipped" section, last action of the job, no other root-STATUS.md edits permitted.

---

## 11. Dispatch breadcrumb — append one line to root STATUS.md as your last action

As the **absolute final action** of any dispatched job, append one line to the orchestrator's root `STATUS.md` (path: `../STATUS.md` from worker CWD) at the top of the **Recently shipped (last 7 days)** section.

**Why:** future-orchestrator can answer "did the dispatch land?" from a single auto-loaded file (root STATUS.md is read first on every session). Removes the operator-as-message-bus dependency.

**Format (one line, exact):**

```
YYYY-MM-DD HH:MM — [worker-name] [STATUS] [slug-or-task] → [artifact paths, comma-separated]
```

- `[worker-name]` = `design-claude`, `content-claude`, `va`, or any custom worker name
- `[STATUS]` = one of:
  - `SHIPPED` — full success, all deliverables produced
  - `PARTIAL` — some deliverables produced, others blocked or deferred (include short reason)
  - `BLOCKED` — could not complete, see escalation file
- `[slug-or-task]` = the slug or short task identifier from your dispatch
- `[artifact paths]` = relative paths from project root to what you produced (or `escalation: [path]` for BLOCKED)

**Examples:**

```
2026-05-05 16:42 — design-claude SHIPPED weekly-dashboard → design-claude/final/cover_topic.png, daily/THIS-WEEK.html
2026-05-05 17:08 — content-claude SHIPPED topic-caption → content-claude/posts/post-topic.md
2026-05-05 18:15 — design-claude PARTIAL topic-redo → cover rebuilt; dashboard re-embed deferred (caption MD not yet committed)
```

**Hard rules:**

- One line, no narrative. Multi-line summaries belong in the worker's own sandbox STATUS.md.
- Append at the **top** of "Recently shipped" (newest first). Don't reorder existing entries.
- This is the **only** edit a worker may make to root STATUS.md (§ 10 exception). Don't touch Active threads / Next moves / Blocked on operator / Last updated stamp — those are orchestrator-owned.
- Cost target: <50 tokens per breadcrumb. If you find yourself writing more than one line, you're outside this rule.
- Skip the breadcrumb only if the dispatch was operator-direct (no formal worker session — e.g. a quick file edit the operator asked you to run inline). Every paste-prompt dispatch gets a breadcrumb.

---

*Add new shared rules to this file rather than inlining them in sandbox `CLAUDE.md` files. Per ICM, Layer 3 reference material is shared across all workers; per-worker exceptions go in the sandbox CLAUDE.md only when the rule genuinely doesn't apply elsewhere.*
