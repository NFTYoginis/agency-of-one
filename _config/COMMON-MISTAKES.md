# COMMON-MISTAKES.md — Anti-patterns and how to avoid them

> Project-specific anti-patterns. Loaded on demand (not auto-loaded). Read this when starting a session if you suspect you're about to repeat one of these. Each entry: what the mistake looks like → why it breaks → the fix.

---

## 0. Generating labeled illustrations without saving the render script

**What happens:** A session generates labeled figure PNGs (anatomy diagrams, charts, infographics) with positioned text labels via SVG → Puppeteer. The PNG ships. The render script is never committed. Weeks later, a label is found to be truncated (text-anchor:end with too-small left margin → leading characters fall past x=0). The fix needs the original render pipeline, which doesn't exist.

**Why it breaks:** Without the source script, the only fix paths are (a) recreate the entire pipeline from scratch (hours of work + regression risk on every consumer of the PNG) or (b) PNG paint-over via `sharp` (surgical but not reproducible). Both are downstream of the real failure: ephemeral generation.

**Fix:** When generating any labeled figure with positioned text, the render script gets committed alongside the PNG output, with a header comment naming every input PNG it produces. If the figure has labels on the LEFT side using `text-anchor:end`, build in a minimum left margin (~30px from canvas x=0) to prevent truncation. The kill-switch in any cleanup brief: if the original render script can't be located, escalate rather than recreate.

---

## 1. Regenerating the daily MD when the dashboard is the artifact

**What happens:** Operator says *"execute [date]"*. Orchestrator generates `daily/YYYY-MM-DD.md` with sections, validation checklists, Plan B, operator notes — duplicating what design-claude's rolling `daily/THIS-WEEK.html` already shows.

**Why it breaks:** ~50k tokens for what the architecture was designed to handle in ~5k. The calendar is locked, the worker rolls prior days into the same dashboard, the MD is duplicate work.

**Fix:** Default to dispatch-only. Grep one calendar row → write the design-claude prompt inline → hand off. No MD on routine days. Full MD is opt-in via *"full brief"*. See `briefs/_TODAY-TEMPLATE.md`.

---

## 1a. content-claude (or orchestrator) producing the daily HTML

**What happens:** content-claude or the orchestrator generates `daily/THIS-WEEK.html` (or per-day HTML in the old pattern) before design-claude is dispatched. design-claude later regenerates it on its own dispatch — two HTML generations for one day's work.

**Why it breaks:** Boundary violation. Worker artifact ownership exists for a reason: design-claude is the only role with the brand palette, the rendering scripts, and the dashboard layout in its head. Cross-role HTML generation is always regenerated, always duplicative.

**Fix:** `_config/_WORKER-RULES.md` § 9 (artifact ownership). On the default daily flow: orchestrator dispatches; content-claude has no role unless explicitly cross-dispatched; design-claude alone produces HTML and visuals. When the operator asks the orchestrator for HTML, the cheap answer is the dispatch one-liner — not "let me do it."

---

## 1b. Generating per-day HTMLs instead of the rolling weekly dashboard

**What happens:** Orchestrator (or anyone) writes `daily/YYYY-MM-DD.html` — one file per day — instead of refreshing the single rolling `daily/THIS-WEEK.html`.

**Why it breaks:** Seven HTMLs per week each costs design-claude a regen + a yesterday-MD/HTML read. The rolling dashboard is one file: one regen point, one source of truth, no rollover read needed.

**Fix:** Only `daily/THIS-WEEK.html` exists. design-claude rebuilds it from scratch on the first dispatch of a new week, refreshes today's section in place on subsequent dispatches. See `briefs/_WEEKLY-HTML-TEMPLATE.md`.

---

## 2. Reading source files speculatively

**What happens:** Orchestrator reads the full script, full article body, full post copy, "to give the operator a summary."

**Why it breaks:** The operator opens the source file at execution time. The orchestrator's summary is throwaway context that bloats the session.

**Fix:** Reference, don't inline. Path + hook line is enough. Operator opens the file when ready to post or film.

---

## 3. Loading the full week section / full template

**What happens:** Orchestrator reads the full calendar (~600 lines) when only one row was needed. Or reads the full `_TODAY-TEMPLATE.md` (~135 lines) on a routine day.

**Why it breaks:** Single biggest token waste in this setup. CLAUDE.md explicitly calls this out: *"Reading 644 lines to extract 30 is the most expensive habit."*

**Fix:** Bash grep to find the section, then Read with `offset` + `limit` for just the slice. Routine days don't read the full template at all.

---

## 4. Reading prior-day artifacts to "roll forward"

**What happens:** Orchestrator reads prior-day MDs or `daily/THIS-WEEK.html` to know what to put in today's brief.

**Why it breaks:** That's the worker's job. design-claude reads the existing dashboard when refreshing it. Orchestrator duplicating that work is the daily-MD regression in another shape.

**Fix:** Orchestrator never reads prior-day artifacts on a routine day. Worker owns rollover.

---

## 5. Skipping the "Skip These" column in CONTEXT.md

**What happens:** Worker (or orchestrator) reads only the Load column and ignores the Skip column. Loads "related-looking" files just-in-case.

**Why it breaks:** The Skip column is the token budget. Ignoring it is exactly the failure mode that loaded everything before the skip column existed.

**Fix:** Treat Skip as a hard rule, not a suggestion. If a file is in the Skip column for your task, do not open it unless your brief explicitly overrides.

---

## 5a. Two-pass HTML — placeholder tiles, then real previews

**What happens:** design-claude ships `daily/THIS-WEEK.html` with `.pending-tile` placeholders ("asset coming") in the first dispatch, then regenerates the same HTML embedding the real cover previews after the cover scripts complete. Two HTML generations for one day's deliverables.

**Why it breaks:** The dashboard is meant to be single-pass. Covers and HTML produce together; the HTML embeds real previews on the same dispatch. Placeholders mean the worker is rendering ahead of its own output — pointless intermediate state.

**Fix:** `briefs/_WEEKLY-HTML-TEMPLATE.md` Section 1 — covers and dashboard ship in a single pass with real previews embedded. No `.pending-tile` CSS, no pre-render stubs. If cover generation fails (parse the JSON `status_text`, not stdio), escalate before producing the HTML.

---

## 5b. Deferring phrase/slug/category to the worker

**What happens:** Dispatch prompt says *"design-claude picks one verbatim phrase from REFERENCE.md"* and *"slug picked by design-claude."* Worker spends ~2k tokens reading REFERENCE.md and reasoning about angles to make a decision the orchestrator could make in ~50 tokens.

**Why it breaks:** The calendar already implies the angle. Pre-decided fields (phrase, slug, category, caption-source, photo-source) are cheap on the orchestrator side and expensive on the worker side. Deferring burns worker context on a creative branch already implicitly closed.

**Fix:** `briefs/_TODAY-TEMPLATE.md` standard dispatch — required pre-decided fields. Orchestrator fills them all before pasting the prompt. Workers don't pick.

---

## 5c. Inventing captions when the source MD is missing

**What happens:** Dispatch doesn't specify a caption source path or `operator-live`. Worker writes its own caption to fill the dashboard card. Voice drift, AI-isms, no `humanizer` pass.

**Why it breaks:** Caption authorship is content-claude's lane (or the operator's, live at post time). design-claude inventing copy violates the worker boundary AND skips the `humanizer` skill activation gate.

**Fix:** `briefs/_TODAY-TEMPLATE.md` requires the dispatch's `caption` field to be set to either a path or `operator-live`. design-claude escalates if the field is missing — never invents.

---

## 6. Skill listed but not triggered

**What happens:** A skill like `/humanizer` is "available" but no one runs it. Drafts move to `final/` with AI-isms intact, then get caught by the operator on review.

**Why it breaks:** Available ≠ active. If the trigger condition is fuzzy, the worker skips it.

**Fix:** Skills must be wired in `_config/_WORKER-RULES.md` § 7 (skill activation) with explicit trigger condition. *"Before any draft moves to `final/`"* is a trigger. *"Available"* is not.

---

## 7. Generating a full brief on a clean calendar day

**What happens:** Orchestrator builds a 150-line MD with per-deliverable sections, validation checklists, Plan B, etc. — when the calendar row is unambiguous and the worker can execute from one line.

**Why it breaks:** The full-brief mode exists for ambiguous days. Using it as the default makes every day expensive.

**Fix:** Full-brief mode is opt-in only. Triggers: operator says *"full brief"* / *"detailed plan"* / *"inline content"*, OR the calendar row has multiple candidate angles + no clear default.

---

## 8. Cross-sandbox writes without brief authorization

**What happens:** Worker (e.g., content-claude) edits a file outside its sandbox — the active calendar, a `_config/` file, another sandbox's folder.

**Why it breaks:** Creates cross-sandbox drift that's expensive to diagnose later. Voice rules, calendar rows, brand tokens all need a single source of truth.

**Fix:** `_WORKER-RULES.md` § 1 hard rule. Workers read project-level files when their brief's Inputs table requires it; they never write to them. The brief's Returns-with section is the only authorization that crosses the boundary.

---

## 9. Updating the per-deliverable tracker before the operator confirms

**What happens:** Worker delivers a draft and marks the calendar/status tracker as live/posted.

**Why it breaks:** Status reflects what's *live on platforms*, not what's *been written*. Drafts in `final/` aren't posted; they're ready to post. Premature checkmarks corrupt the tracker.

**Fix:** `_WORKER-RULES.md` § 3. Status updates only after operator confirms live. Worker leaves the update to the orchestrator.

---

## 10. Apologies and contrition padding

**What happens:** Worker output starts with *"I apologize for the confusion,"* / *"sorry about that,"* / three sentences of self-flagellation before the actual fix.

**Why it breaks:** Wastes tokens, doesn't change the outcome, and signals the worker is performing remorse instead of solving the problem.

**Fix:** `_WORKER-RULES.md` § 6. One sentence: what went wrong + the corrected output. Move on.

---

## 11. Iterating past three strikes instead of escalating

**What happens:** Worker rewrites the same output a fourth, fifth, sixth time based on feedback that keeps shifting.

**Why it breaks:** Three identical-shape rewrites means the brief is wrong, not the worker. The source needs editing, not the binary.

**Fix:** `_WORKER-RULES.md` § 8 (three-strike rule). After three rewrites, stop and write to `briefs/questions/<slug>-question.md`. Surface what was tried, what was wanted, the gap, 2–3 paths forward.

---

## When to update this file

Add a new entry when a regression costs measurable time/tokens and is likely to recur. Each entry should have: what the mistake looks like, why it breaks, the fix. Date the catch in the *"Caught"* line so future-you can judge whether the entry is still load-bearing.

Stale entries: if a mistake hasn't recurred in 60+ days and the architecture has changed enough that the failure mode no longer makes sense, archive it (don't just delete — the historical record is useful).
