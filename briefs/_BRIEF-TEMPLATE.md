# <slug>

**Worker:** [content-claude | design-claude | va | <custom-worker>]
**Sandbox:** [path to sandbox entry point — e.g. `content-claude/CLAUDE.md`]
**Date:** [YYYY-MM-DD]

---

## Orchestrator pre-draft check (before writing this brief)

Run before filling the sections below. Cuts scope creep at the cheapest moment:

- [ ] Is anything in this brief out of scope for the current sprint / week?
- [ ] Is anything too complex for this stage and better deferred?
- [ ] Could this be split into 2 smaller briefs (research + execution)?
- [ ] Are all the source files actually ready, or am I dispatching against placeholders?
- [ ] Does this brief stay under ~200 lines? If not, it likely contains multiple stages — split.

If any answer is "yes, prune," prune now. The cheapest time to cut scope is before any work exists.

---

## Task

One paragraph. The outcome only — what done looks like in prose. Not the steps. Not the approach. The result.

---

## Inputs

Files the worker must read before starting, separated by ICM layer. Layer 3 = reference (rules to internalize). Layer 4 = working artifacts (this run's source material).

| Layer | File | Why it matters | Sections to focus on |
| --- | --- | --- | --- |
| 3 (reference) | `_config/BRAND.md` | voice rules, key phrases, what to avoid | §3 voice rules, §4 key phrases |
| 3 (reference) | `_config/REFERENCE.md` | brand tokens, file naming, locked phrases | as needed |
| 4 (working) | `[path to this-run's source]` | the input being transformed | [section] |
| 4 (working) | `[path to handoff from prior stage]` | what the previous stage produced | [section] |

Workers must NOT load files that aren't in this table. If a file seems missing, escalate — do not load speculatively.

---

## Scope

**In-scope:**
- [what the worker is allowed to create or modify]

**Out-of-scope:**
- [what the worker must not touch]

**Kill-switch:** If [time threshold or complexity threshold], stop and escalate rather than guessing or expanding scope.

---

## Acceptance

Binary only. True or false. No subjective language.

- [ ] `[exact file path]` exists
- [ ] `[exact file path]` exists
- [ ] Per-deliverable tracker updated with new entry
- [ ] [Any other verifiable condition]

---

## Verify

Cross-stage checks the worker runs *before* returning output to the operator. Each is binary. Worker re-reads its output against the source and confirms each line. Catch issues here so the operator's review surfaces decisions, not defects.

- [ ] Output passes all `_config/BRAND.md` voice rules (no banned phrases, no AI tells, em-dash count ≤1/page, zero emojis)
- [ ] Every concrete fact, name, date, or quote is either verified in the Inputs above or marked `[Placeholder: …]`
- [ ] Output references the calendar entry / brief / prior stage it serves (no orphaned content)
- [ ] No invented file paths or invented `_config/` references — every link points to a file that exists
- [ ] **File-type permissions:** files produced match the file types named in Returns-with. No extra formats (e.g. do not generate a PDF if Returns-with says `.md` only). If a useful additional format suggests itself, escalate; do not ship it.
- [ ] **URL / referral allowlist:** any URLs, affiliate links, or referral codes inserted into output are either named in this brief's Inputs/Task or supplied by the operator. No referral codes pulled from external sources without explicit authorization.
- [ ] [Any task-specific verification]

If any verify check fails, fix it before returning. If a check is impossible to verify (e.g. blocked by missing reference material), escalate.

---

## Escalation

If ambiguity hits at any point, write the question to:

`briefs/questions/<slug>-question.md`

Then stop. Do not guess. Do not expand scope. The orchestrator reads it next session.

---

## Returns-with

What the worker produces before closing the session.

- [ ] `[file 1 at exact path]`
- [ ] `[file 2 at exact path]`
- [ ] `[file 3 at exact path]`
- [ ] Confirmation that the per-deliverable tracker is updated (if applicable)
