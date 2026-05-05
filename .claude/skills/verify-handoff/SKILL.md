---
name: verify-handoff
description: Cross-check a worker's shipped output against the dispatching brief's Inputs/Outputs/Verify sections. Catches the class of defect where a file exists but its content is wrong (e.g., caption MD existed but wasn't embedded in the dashboard). Use after a worker breadcrumb lands, before declaring a session shipped, or when the operator says "verify [slug]" / "check the handoff" / "did [worker] actually do it right". Implements ICM paper § 6.2 cross-stage trace verification. One brief slug or path as input; outputs a PASS/FAIL/MANUAL report. Does not modify files.
---

# verify-handoff

Confirm that what the worker shipped matches what the brief asked for. Closes the gap between "file exists" (cheap, misleading) and "file is correct" (expensive, useful).

This skill is the operator-side analogue of the worker's own Verify section in the brief. The worker runs Verify before returning; this skill runs the same checks from the orchestrator's seat to catch cases where the worker's self-check was incomplete.

## When to invoke

- **After a worker breadcrumb lands** in root `STATUS.md` "Recently shipped."
- **Before session-end** — orchestrator's last sanity check before declaring the session shipped.
- **Operator asks** "verify [slug]" / "check the handoff" / "did [worker] actually do it right" / "does [path] match the brief."
- **After a `-redo` dispatch** — confirm the redo fixed the original defect.

Skip when: the operator already manually verified inline; the brief was a quick edit with no formal Returns-with section; the dispatch was operator-direct without a brief file.

## Inputs

One argument. Any of:

- **Brief slug** — e.g., `topic-redo`. Skill resolves to `briefs/YYYY-MM-<slug>.md` or similar.
- **Brief path** — e.g., `briefs/2026-05-html-calendar-sync.md`. Skill reads directly.
- **Breadcrumb line** — pasted from STATUS.md. Skill parses worker + slug + paths.
- **No argument** — read the most recent breadcrumb from root `STATUS.md` "Recently shipped" and verify that one.

## What to check

### Always-checks (run regardless of brief structure)

1. **Every output exists.** Parse the brief's `Returns-with` (or `Outputs`) section. For each path, confirm the file is on disk via Read or `ls`.
2. **Output is recent.** mtime within 24h of the breadcrumb timestamp (or within 1h for same-session dispatch). Stale mtime = worker may have shipped a previous run's artifact.
3. **Inputs were readable.** For each path in the brief's Inputs table, confirm it exists. A worker that shipped without one of its declared inputs either guessed or skipped — flag.
4. **Slug consistency.** Worker's breadcrumb slug matches the brief filename. Drift signals a renamed dispatch that lost its trail.

### Format-specific automatic checks

| Output type | Checks |
| --- | --- |
| **PNG** | `sips -g pixelWidth -g pixelHeight` — does dimension match brief spec? File size sanity (>10 KB, not a 1×1 pixel). |
| **HTML** (e.g., `daily/THIS-WEEK.html`) | Parses without obvious truncation. Contains the slug from the brief. **If the brief Inputs include a caption MD, the HTML body contains a substring (15+ consecutive chars) from that caption MD.** This is the caption-embedding check — caption was synthesized, not embedded. |
| **MD** | Non-empty (>200 chars). For post MDs: contains `caption` and `hashtags` blocks. For article briefs: contains expected H2 sections per voice rules. |
| **PDF** | File parses (basic header check). Page count matches brief if specified. |

### Brief Verify section

If the brief has a `## Verify` section (per `briefs/_BRIEF-TEMPLATE.md`), run each line literally:

- Voice-rule checks → run `/humanizer` mentally or Read against `_config/BRAND.md` voice rules.
- "Every fact verified or marked Placeholder" → grep output for `[Placeholder:` and confirm; spot-check 2–3 facts against Inputs.
- "No invented file paths" → for any path-shaped string in output, confirm the file exists.
- "No unauthorized URLs" → diff URLs in output against URLs in brief Inputs/Task. Flag novel ones.

Each line produces PASS / FAIL / MANUAL.

- **PASS** — the skill ran the check and it passed.
- **FAIL** — the skill ran the check and it failed; cite the specific evidence.
- **MANUAL** — the check requires human judgment (e.g., "voice matches article-02's register"). List as needing operator eye.

## Output structure

```
# verify-handoff: [brief-slug]

**Brief:** [path]
**Worker:** [content-claude / design-claude / etc.]
**Breadcrumb:** [the line from STATUS.md, verbatim]

## Always-checks
- [PASS/FAIL] every output exists — [N of M present]
- [PASS/FAIL] mtime within window — [output mtime] vs [breadcrumb time]
- [PASS/FAIL] inputs all readable — [N of M readable]
- [PASS/FAIL] slug consistent

## Format-specific checks
- [PASS/FAIL] [check name]: [detail or evidence]

## Brief Verify section
- [PASS/FAIL/MANUAL] [criterion verbatim from brief]: [detail]
- [...]

## Manual verify suggested
- [things the skill can't auto-check, with one-line guidance]

## Verdict
**[CLEAN | DEFECTS | NEEDS-MANUAL]** — [one-sentence summary]

[If DEFECTS: list specific defects with brief: file, what's wrong, suggested action.]
```

## Anti-patterns (don't do these)

- **Don't trust file existence as success.** Always read enough of the file to confirm structural correctness, especially for HTML caption embedding.
- **Don't escalate one-PASS-failure to DEFECTS verdict.** Some failures are expected (manual-verify items, optional fields). Use the verdict line to summarize, not the count.
- **Don't write to STATUS.md or any file.** Output a report; operator decides what to do (re-dispatch, accept-as-is, or escalate).
- **Don't run automatically on every dispatch.** Cost per run isn't free. Run on-demand or as a session-end check, not as a default post-tool hook.
- **Don't infer verify criteria the brief didn't specify.** If the brief's Verify section is empty, run only Always-checks + Format-specific checks. Don't invent criteria from voice rules unless the brief invoked them.
- **Don't fix what you find.** The skill diagnoses; the operator dispatches a redo or accepts. Auto-fixing crosses the worker boundary (per `_config/_WORKER-RULES.md` § 1).

## Verify (skill self-check before returning)

- [ ] Every check that ran is labeled PASS / FAIL / MANUAL — no ambiguous language.
- [ ] Verdict line names DEFECTS only if at least one always-check or format-check FAILED, or a brief-Verify item FAILED with concrete evidence.
- [ ] No file was edited.
- [ ] If the brief had no Verify section, the report says so explicitly (so operator knows the gap is in the brief, not the skill).
