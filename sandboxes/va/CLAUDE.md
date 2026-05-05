# va — Handoff team sandbox

Handoff-ready files prepared for a VA, contractor, or freelancer to execute against. The orchestrator drafts the build pack here; once handed off, the files are **read-only** to all workers (and to Claude sessions inside the project) until the operator explicitly authorizes changes.

Check [STATUS.md](STATUS.md) first — if the request is a small follow-up already mapped there, you may not need anything else. Otherwise: read `CONTEXT.md`, then any active build pack in this sandbox.

Update STATUS.md at end of any session that ships a build pack, fields a question from the handoff team, or shifts a thread (per `../_config/_WORKER-RULES.md` § 10).

---

## Cross-cutting worker rules

Read `../_config/_WORKER-RULES.md` before any file operation. Sandbox boundary, memory rules, status tracking, voice rules, escalation — single source of truth shared across all workers.

---

## What this worker produces

Files that a human downstream is going to execute against. The deliverable is the **handoff package** itself — every spec, every checklist, every screenshot the VA needs to do the work without re-asking. Nothing more, nothing less.

Typical contents of a handoff package:

- `<project>-Build-Brief.html` (or `.md`) — full context for the build: what we're making, why, scope, links to all source files
- `<project>-Page-Specs.html` (or `.md`) — per-page / per-asset spec sheet: titles, slugs, meta, OG image, CTA
- `<project>-Build-Checklist.md` — dependency-ordered task list, broken into phases the VA can check off
- `<project>-Punch-List-YYYY-MM-DD.md` — round-N feedback after the VA delivers a draft

The exact shape varies per project. Keep filenames stable across handoff rounds — version via `-v2`, `-Punch-List-YYYY-MM-DD`, etc., not via filename rename.

---

## Folder Structure

```text
va/
├── CLAUDE.md                                ← this file
├── CONTEXT.md                               ← current handoff context
├── STATUS.md                                ← active build packs, recently shipped
├── briefs/                                  ← briefs received from orchestrator
└── [project-name]/
    ├── [project]-Build-Brief.html
    ├── [project]-Page-Specs.html
    ├── [project]-Build-Checklist.md
    ├── [project]-Punch-List-YYYY-MM-DD.md
    └── assets/                              ← any source files / OG images / screenshots referenced by the brief
```

---

## The no-edit-after-handoff rule (hard rule)

Once a build pack is **handed off to the VA** (operator confirms the link/folder has been shared), no worker — and no orchestrator session — edits the pack files until the operator authorizes a change. The reason: the VA is executing against a snapshot. Edits to the snapshot mid-execution corrupt the contract.

When the operator wants to update a handed-off pack, the routine is:

1. Operator names the change (e.g., "the OG image for page 3 needs the new headline")
2. Worker writes the change as a **punch-list entry** (`<project>-Punch-List-YYYY-MM-DD.md`), not as an edit to the original spec
3. Operator forwards the punch-list to the VA explicitly
4. Spec files only get modified if a *new* round of work starts — and then the original gets archived under `_archive-handoff-r1/` first

This is enforced (lightly) by the `handoff-files-guard.py` hook — the operator populates `HANDOFF_MARKERS` in that file with path fragments specific to active build packs, and the hook prompts before any edit lands. The hook is informational, not blocking; the discipline is the rule, not the hook.

---

## Build-checklist convention

Every build package includes a `<project>-Build-Checklist.md` that's dependency-ordered into phases. The VA executes top-to-bottom. Each phase has:

- A one-line goal
- The pages / assets / actions in dependency order (asset upload → page build → automation wiring → email queue → publish)
- A checkbox per item (`[ ]` / `[x]`)
- An "exit criteria" line for the phase (what's true when this phase is done)

Phases are sized so the VA can finish one in a single working session. If a phase needs more than one session, split it.

---

## Output Rules

- All work stays in `va/` and is paired with a project-named subfolder
- Build packs are operator-curated — workers draft, but the operator reviews + ships
- Update the per-deliverable tracker only when the operator confirms the VA has delivered (not when the pack is shipped to the VA — the pack is a contract, not a deliverable)
- Cross-references to `_config/`, content sandboxes, or design assets use `../` paths so the VA's preview links work without the build pack being moved
