# MEMORY — Auto-loaded index

> This file is the always-loaded index for the operator's auto-memory. Claude Code reads this on every session and treats it as the entry point to scoped memory subfolders. Each line below is a pointer to a memory file (`name.md` with frontmatter), not the memory content itself. Keep entries under ~150 chars; truncate if needed.

> **How auto-memory works:** memory files live under `~/.claude/projects/-<flattened-project-path>/memory/`. They have YAML frontmatter (name, description, type) and short bodies. Claude reads `MEMORY.md` to decide which deeper memory file to open per task. Types: `user` (who you are), `feedback` (corrections/preferences), `project` (in-flight initiatives), `reference` (where to look for things).

> Do **not** write memory content directly into this file. Use it as a one-line-per-entry index.

---

## Global (loaded every session)

> Pointers to `_global/` memory files — facts that apply across all sandboxes. Operator role, top-level preferences, cross-cutting feedback.

- _no entries yet — write your first global memory and link it here_

## Orchestrator-scoped

> Pointers to `orchestrator/` memory files — initiatives the orchestrator is steering, decisions in flight, recent retrospectives that should still inform planning.

- _no entries yet_

## Worker-scoped (when populated)

> Pointers to per-worker memory files — `content-claude/`, `design-claude/`, `va/`, etc. These load only when the named worker starts a session inside its sandbox. Keep worker memory tight: feedback the worker should remember, not project state (which lives in the worker's `STATUS.md`).

- _no entries yet_

---

*Stale-memory rule: a memory file that hasn't been read or referenced in 90 days is a candidate for archive at the next monthly maintenance pass. The audit doesn't auto-delete — it surfaces the entry to the operator, who decides.*
