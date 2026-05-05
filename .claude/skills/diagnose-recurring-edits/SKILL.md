---
name: diagnose-recurring-edits
description: Aggregate breadcrumbs, escalations, and audit logs from the last 14–30 days to surface recurring correction patterns that should be fixed at the source level (brief template, _config/, _WORKER-RULES.md) rather than re-fixed each session. Use during weekly maintenance Phase 2, after a redo dispatch, or when the operator says "diagnose patterns" / "what keeps breaking" / "edit-source candidates" / "recurring fixes". Implements the edit-source feedback loop from ICM paper § 6.3 — pairs with the three-strike rule (`_config/_WORKER-RULES.md` § 8) and dispatch-breadcrumb rule (§ 11). Closes the loop between worker corrections and durable system improvements.
---

# diagnose-recurring-edits

Watch the breadcrumb trail. Find the patterns. Propose source-level fixes. Don't apply them — operator validates during weekly maintenance Phase 3.

This is the orchestrator's diagnostic skill. Workers self-flag (per § 8 three-strike); this skill aggregates across workers and across sessions to find patterns no single worker can see.

## When to invoke

- **Weekly maintenance Phase 2** — surface source candidates *before* operator validation gate.
- **After a `-redo` / `-fix` / `-v2` dispatch** — check if this is a one-off or part of a pattern.
- **Operator asks** "what keeps breaking" / "diagnose patterns" / "edit-source candidates" / "recurring fixes."

Skip when: the operator wants a one-off correction; nothing has shipped in the last 14 days; this skill ran less than 3 days ago (results will be near-identical).

## What to read (in this order)

Read each one with `Read` (not Bash cat). Skip files that don't exist — most sandboxes have a `STATUS.md` but a few may not yet.

1. **Root [STATUS.md](../../../STATUS.md)** "Recently shipped" — last 14 days of breadcrumbs.
2. **Sandbox STATUS.md files** — every sandbox in the project root. Same parsing rules.
3. **`briefs/questions/`** directory listing — every file is an escalation per `_config/_WORKER-RULES.md` § 5. Read each.
4. **`briefs/_MONTHLY-AUDIT-LOG.md`** if present — patterns logged from prior monthly sweeps.
5. **`_log/RETROSPECTIVES.md`** if present — weekly retrospective entries.

**Do not read worker session conversation history.** The breadcrumb + escalation surfaces are designed to compress that signal. Reading conversations re-introduces the noise the breadcrumbs were meant to filter.

## Pattern-detection heuristics

A signal is a **pattern** (not a one-off) when at least one of these holds:

| Threshold | What to look for | Example |
| --- | --- | --- |
| **3+ same-shape corrections in 30 days** | Slug pairs ending in `-redo`/`-fix`/`-v2` with the same root cause | three different cover redos all caused by missing caption MD |
| **Same worker self-flags the same defect class twice** | Worker breadcrumb shows `PARTIAL` or post-hoc fix-up for the same kind of issue | design-claude flags "caption text wasn't embedded" twice |
| **Same brief field omitted across 3+ dispatches** | Briefs in `briefs/` lacking the same field, surfaced via escalations | three briefs missing `photo-source` field |
| **Same escalation question recurs** | Two `briefs/questions/*` files asking effectively the same thing | two question files about hashtag count |

A signal that fires once is a **one-off**. Note it but do not propose a source-level change. Section 6.3 of the ICM paper is explicit: "Sometimes the output needs a human touch that cannot be reduced to a source-level rule."

## Output structure

Write one report to the conversation. Do not edit any file.

```
# Recurring-edit diagnosis — YYYY-MM-DD

Window: [start date] -> today (N days)
Sources scanned: [list of STATUS files + escalations + logs]

## Patterns detected

### 1. [One-line pattern name]
**Evidence (>=3 occurrences or 2+ self-flags):**
- YYYY-MM-DD — [worker] [STATUS] [slug] — [what happened, one sentence]
- YYYY-MM-DD — [...]
- YYYY-MM-DD — [...]

**Source-level fix candidate:** [specific file + section, e.g., "amend `briefs/_BRIEF-TEMPLATE.md` Inputs section to require photo-source field"]
**Why source, not output:** [one sentence — what makes this cross-run, not per-run]
**Estimated cost to apply:** [trivial / minor / structural]

### 2. [...]

## Notable one-offs (single occurrence, no fix proposed)

- YYYY-MM-DD — [what happened] — [why it's a one-off, not a pattern]

## No-action recommended

[Instances where the breadcrumb looked like a defect but is actually correct behavior — operator-directed taste edits, intentional creative fine-tunes, etc.]

## Open questions for the operator

- [Anything ambiguous]
```

## Anti-patterns (don't do these)

- **Don't propose fixes for one-off corrections.** Per ICM § 6.3: creative content gets occasional fine-tunes that aren't system defects. The "Why source, not output" line is the test — if you can't write it cleanly, it's a one-off.
- **Don't surface architecture-level changes.** This skill's output is rule edits, brief-template amendments, and `_config/` updates. Anything bigger needs its own dispatch.
- **Don't write to memory or edit files.** Output a report; operator decides what to apply during weekly maintenance Phase 3 (validation gate).
- **Don't re-propose rejected ideas.** If a prior diagnosis was rejected, weekly maintenance Phase 3 logs the rejection — check for it before re-surfacing.
- **Don't bundle unrelated patterns into one suggestion.** If two patterns share a root cause, say so explicitly; otherwise list them separately.
- **Don't read the conversation history.** Breadcrumbs are the durable signal. Conversations are noise.

## Verify (skill self-check before returning)

- [ ] Each "pattern detected" has >=3 evidence lines or >=2 same-worker self-flags.
- [ ] Each pattern has a "Why source, not output" justification.
- [ ] No file was edited.
- [ ] Window dates are absolute (YYYY-MM-DD), not relative ("last week").
- [ ] One-offs are listed separately; nothing in "patterns" section has only 1 evidence line.
