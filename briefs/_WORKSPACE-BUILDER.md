# _WORKSPACE-BUILDER.md — Spin up a new worker sandbox

> Per ICM §4.4 (workspace-builder). Takes a 9-question questionnaire from the operator and produces a new sandbox folder with all project conventions baked in, plus the cross-cutting registry updates that make the new worker visible to the orchestrator. Run by the orchestrator. Workers do not run this on themselves.

---

## When to use

- A new worker is being added to the system (e.g. `fb-ads-claude`, `coaching-claude`, future workers)
- An existing sandbox is being restructured significantly enough that a clean rebuild beats incremental edits
- The operator wants to test a workflow domain before committing to a permanent worker

Do NOT use this for routine content edits or to rename one folder. Workspace-builder is for whole-sandbox creation.

**Worker training material:** if you keep raw source material (transcripts, course notes, reference recordings) outside the project folder, point the new worker's first dispatch at the relevant subfolder. Worker absorbs → distills into its own CLAUDE.md / CONTEXT.md / brief templates → source goes quiet.

---

## The questionnaire (operator answers before execution)

The orchestrator asks the operator these nine questions. If the operator can't answer one, escalate — do not invent.

1. **Worker name** — exact handle (e.g. `fb-ads-claude`, `coaching-claude`). Lowercase, hyphenated.
2. **Sandbox folder name** — exact path under project root. Match existing convention.
3. **One-paragraph mandate** — what does this worker produce? Plain English, 3–5 sentences. No hype.
4. **Output types** — comma-separated list of the artifacts this worker ships (e.g. *"ad copy variants, audience targeting specs, A/B test plans"*).
5. **Output folder structure** — 3–5 subfolders inside the sandbox, with a one-line purpose each.
6. **File naming convention** — pattern with placeholders (e.g. `ad-[campaign]-[variant].md`). Match existing convention style.
7. **Required `_config/` reads** — which Layer 3 files this worker loads by default (typically `_config/BRAND.md` + `_config/REFERENCE.md`; sometimes `_config/RELATED_PROJECTS.md`).
8. **Voice / register notes** — anything voice-specific to this domain that goes BEYOND `_config/BRAND.md`. If nothing extra, write *"Use `_config/BRAND.md` rules as-is."*
9. **Pillar mapping** — which of your pillars this worker primarily serves, and which it supports.

---

## Execution checklist (orchestrator runs in this order)

### Phase 1 — Sandbox folder

1. `mkdir -p [sandbox-folder]/[output-subfolder-1]/`, etc., for each subfolder from Q5.
2. Write `[sandbox-folder]/CLAUDE.md` using the template below. Substitute every `{{placeholder}}` from the questionnaire answers.
3. Write `[sandbox-folder]/CONTEXT.md` using the CONTEXT template below.
4. Write `[sandbox-folder]/STATUS.md` as an empty template per `_config/_WORKER-RULES.md` § 10.
5. Add a `[sandbox-folder]/briefs/` folder if the worker will receive briefs locally (most do).

### Phase 2 — Cross-cutting registry updates

6. **Root `CLAUDE.md`** — add a new row to the `## SANDBOXES` table:
   `| \`{{sandbox}}/\` | {{one-line summary}} | \`{{sandbox}}/CLAUDE.md\` |`
7. **Root `CONTEXT.md`** — add row(s) to the `## What to Load for Each Task Type` table. One row per common task this worker handles.
8. **`MEMORY.md`** (in user memory folder) — confirm a `memory/{{worker-shortname}}/` subfolder exists; if not, create it. Update the Scopes table if this is a new worker type.
9. **Root `_config/REFERENCE.md`** — add the new naming convention to the file-naming table.

### Phase 3 — Smoke test

10. Confirm the sandbox is reachable: open `[sandbox-folder]/CLAUDE.md` mentally; can a fresh Claude session read it cold and know what to do? If yes, ship. If no, fix.
11. Tell the operator the sandbox is ready, the entry point, and the first task they can dispatch into it.

---

## Templates

### Sandbox `CLAUDE.md` template

```markdown
# {{sandbox-folder-name}}

{{one-paragraph mandate from Q3}}

Read `CONTEXT.md` for current priorities and what to load per task. Read root `_config/BRAND.md` for voice rules. Read root `_config/REFERENCE.md` for brand tokens, file naming, locked phrases.

---

## Cross-cutting worker rules

Read `_config/_WORKER-RULES.md` before any file operation. Sandbox boundary, memory rules, status tracking, voice rules, escalation — single source of truth shared across all workers.

---

## What this worker produces

{{output types from Q4}}

---

## Folder structure

\```text
{{sandbox-folder-name}}/
├── CLAUDE.md                ← this file
├── CONTEXT.md               ← current priorities, task loading
├── STATUS.md                ← active threads, next moves, recently shipped
{{output subfolders from Q5, formatted as tree}}
└── briefs/                  ← briefs received from orchestrator
\```

---

## Voice & register

{{Q8 — voice notes specific to this worker, or "Use _config/BRAND.md rules as-is."}}

---

## Pillar mapping

Primary: {{pillar from Q9}}
Supporting: {{other pillars}}

---

## Output rules

- All work saved as `.md` files in the correct subfolder unless explicitly otherwise (e.g. PNG for design)
- Naming: `{{naming convention from Q6}}`
- Update the per-deliverable tracker (project root) when an item is shipped, NOT when drafted
- Never write to other sandboxes — handoffs go through briefs in the destination sandbox's `briefs/` folder
```

### Sandbox `CONTEXT.md` template

```markdown
# {{sandbox-folder-name}} — Context

Read after CLAUDE.md.

---

## Current priorities

[Populated by orchestrator when first brief arrives. Until then: "No active work — awaiting first brief."]

---

## Reference Exemplars — calibrate against the real thing

Adjective-based rules drift. Concrete exemplars don't. Before working in any format, open the canonical reference for that format. After producing, diff your work against it: same rhythm? same density? same restraint? If not, the gap is the rewrite target.

| Format | Canonical exemplar | What it demonstrates |
| --- | --- | --- |
{{one row per output type from Q4 — exemplar starts as TBD until a canonical piece ships}}
| [first output type] | _TBD — orchestrator nominates once first canonical piece ships_ | [one-line hook describing the structural move to imitate] |
| [second output type] | _TBD_ | [hook] |

> **Orchestrator note:** one canonical reference per format. Update only when a clearly stronger piece ships. Do not list "good examples" — pick one per row. Workers comparing against three exemplars get diffuse output; workers comparing against one get tight output.

---

## What to load per task

| Task | Load first | Then load |
| --- | --- | --- |
| [first task type] | `_config/BRAND.md` voice rules | [working file from brief] |
| [second task type] | `_config/REFERENCE.md` brand tokens | [working file from brief] |

---

## Default Inputs (Layer 3 / Layer 4 distinction)

| Layer | File | Why |
| --- | --- | --- |
| 3 | `_config/BRAND.md` | voice + key phrases |
| 3 | `_config/REFERENCE.md` | brand tokens, file naming |
{{other Q7 reads as needed}}
| 4 | per-brief working files | named in each brief's Inputs table |

Workers do not load files outside this list speculatively. If a brief requires more, the brief's Inputs table names them.
```

---

## What workspace-builder does NOT do

- Does not write any actual content (briefs, articles, ad copy) into the new sandbox — only structure
- Does not modify other sandboxes — the new sandbox is fully isolated
- Does not auto-dispatch a first brief — operator decides what the new worker does first
- Does not mutate `_config/` — Layer 3 reference material is shared, not per-worker

---

## Verify (run before reporting "ready")

- [ ] Sandbox folder exists with all subfolders from Q5
- [ ] `CLAUDE.md`, `CONTEXT.md`, and `STATUS.md` exist and contain no `{{unfilled-placeholder}}` strings
- [ ] `CONTEXT.md` Reference Exemplars table has one row per output type from Q4 — rows start as TBD; orchestrator fills them in once each format ships its first canonical piece
- [ ] Root `CLAUDE.md` lists the new sandbox in the `SANDBOXES` table
- [ ] Root `CONTEXT.md` has at least one task-routing row pointing to the new sandbox
- [ ] `memory/{{worker-shortname}}/` subfolder exists in user memory
- [ ] `_config/REFERENCE.md` file naming table includes the new convention
- [ ] A fresh session reading the sandbox `CLAUDE.md` cold could execute its first brief without asking what the worker does
