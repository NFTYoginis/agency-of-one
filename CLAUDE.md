# [Your brand] — Master Control

Read this first. Then check [STATUS.md](STATUS.md) for *"where are we / what's next"* — if the operator's request is a small follow-up already mapped there, you may not need anything else. Then `CONTEXT.md` (who, what's active, what to load per task). Then `_config/REFERENCE.md` only when you need a quick lookup. Do not load everything — use STATUS.md and CONTEXT.md to decide which deeper files to open.

Update STATUS.md at end of any session that ships, dispatches, or shifts a thread (per `_config/_WORKER-RULES.md` § 10). Keep it under 60 lines.

---

## Operator triggers (orchestrator routines)

| Trigger phrase | What runs | Spec |
| --- | --- | --- |
| *"prep today"* / *"today's plan"* / *"daily brief"* / *"execute [date]"* | **Default: dispatch-only.** Run pre-flight checklist (slug / caption-MD / cover-PNG / photo) → write paste-prompts inline → hand off in single operator action (parallel-dispatch when multiple workers needed). Worker refreshes the rolling `daily/THIS-WEEK.html` dashboard (no MD, no per-day HTMLs). Target <10k tokens. Full MD brief is opt-in via *"full brief"*. | **Routine: `briefs/_PASTE-SNIPPETS.md`** (paste-templates + pre-flight) · Full spec: `briefs/_TODAY-TEMPLATE.md` · dashboard: `briefs/_WEEKLY-HTML-TEMPLATE.md` |
| *"weekly maintenance"* / *"weekly sweep"* | 4-phase audit: workers purge → orchestrator sweep (incl. token-surface + scan-surface measurement) → operator validation → optional new worker spin-up. Surfaces monthly trigger if first Sunday of month. | `briefs/_WEEKLY-MAINTENANCE.md` |
| *"monthly maintenance"* / *"monthly sweep"* / *"monthly audit"* | Heavier structural compression: auto-trigger `archive [month]` for prior month, monthly audit log update, always-loaded surface compression (MEMORY.md / root CLAUDE.md / sandbox CLAUDE.mds), deeper `_config/` audit, registry consistency, next-month calendar build. Runs first Sunday of each month after weekly. | `briefs/_MONTHLY-MAINTENANCE.md` |
| *"archive [month]"* / *"monthly archive"* / *"sweep posted"* | Move source files (briefs, drafts) for posted prior-month items OUT of the project folder entirely, into the configured external archive location. Rendered outputs (PNGs/PDFs) stay. Workers + orchestrator never scan the Archive folder — operator-only access. Auto-triggered as Phase 1 of monthly maintenance. Delete-on-encounter for duplicates. | `briefs/_ARCHIVE-MONTH.md` |
| *"new worker"* / *"new sandbox"* | 9-question questionnaire that produces a new worker sandbox + cross-cutting registry updates | `briefs/_WORKSPACE-BUILDER.md` |
| *"pending assets"* | Show outstanding asset asks from `briefs/_PENDING-ASSETS.md` | `briefs/_PENDING-ASSETS.md` |
| *"process ideas"* / *"route ideas"* | Route tagged bullets from `ideas.md` to their destination files | `briefs/_IDEAS-PROCESSING.md` |
| *"red team [topic]"* / *"stress-test [topic]"* | Destroy the named plan: list every flawed assumption, second-order effect, and likely failure point. No softening, no balancing positives. Surface 3 most dangerous failure modes. | inline — no spec file |
| *"pre-mortem [topic]"* | Assume the named plan failed 6 months from now. Write the post-mortem as if it already happened. Top 3 reasons in order of probability. Specific and brutal. | inline — no spec file |
| *"build [month] calendar"* / *"new month calendar"* | Build a lean day-by-day calendar for the named month. Daily-posts tables in the live calendar (~200 lines max), strategy/amplifiers in a sibling `_log/<month>-strategy-and-amplifiers.md`. | `briefs/_CALENDAR-TEMPLATE.md` |

---

## WHAT NOT TO DO

- Do not load files speculatively. `CONTEXT.md` routes each task to exactly what it needs — load only that.
- Do not edit handoff-ready files. Anything wired into the `handoff-files-guard.py` hook (or otherwise marked as a downstream contract) is read-only unless explicitly instructed otherwise.
- Do not write in the brand voice without reading `_config/BRAND.md` voice rules and `_config/REFERENCE.md` key phrases first. Honour the banned vocabulary list.
- Do not violate the brand's design rules (backgrounds, overlays, photo direction). See `_config/BRAND.md` § 6 and `_config/REFERENCE.md` Design Specs.
- Do not delete or merge the intentionally duplicated folders. Each worker sandbox keeps its own copies of brand intelligence so it stays self-contained.
- Do not cross sandbox boundaries in a single session. Switch context cleanly.
- Do not update the per-deliverable tracker speculatively. Only update when a deliverable is confirmed complete or confirmed posted.
- Do not Read full files when you only need a slice. For any file over 100 lines on the hot path (`<MONTH>-CALENDAR.md`, `CONTENT-STATUS.md`, sandbox CLAUDE.mds during dispatch, multi-section reference files), use Bash grep to find the section header, then Read with `offset` + `limit` to load only that section. Reading 644 lines to extract 30 is the most expensive habit in this setup.

**Detailed anti-patterns (load on demand):** `_config/COMMON-MISTAKES.md` — entries with what-it-looks-like / why-it-breaks / fix. Read it when you suspect you're about to repeat one.

---

## Architecture decisions (locked)

- **Daily flow is HTML-only by default.** Single rolling `daily/THIS-WEEK.html` produced by design-claude. No per-day MDs in routine flow. Full-brief MD is opt-in via *"full brief"*.
- **Worker boundary on the daily flow.** Orchestrator dispatches; content-claude owns prose source MDs; design-claude alone produces the dashboard HTML and visual assets. Crossing the boundary creates duplicate work. Full rule: `_config/_WORKER-RULES.md` § 9.
- **Required dispatch fields.** Orchestrator pre-decides phrase, slug, category, caption-source, photo-source before dispatching design-claude. Never deferred to the worker. Template: `briefs/_TODAY-TEMPLATE.md`.

---

## Related projects

See [_config/RELATED_PROJECTS.md](_config/RELATED_PROJECTS.md) for properties owned by [your brand].

---

## SANDBOXES

Each has its own CLAUDE.md. Open independently for focused work.

| Folder | What it is | Entry point |
| --- | --- | --- |
| `sandboxes/content-claude/` | Content team sandbox — articles, podcast, social posts, long-form editing | `sandboxes/content-claude/CLAUDE.md` |
| `sandboxes/design-claude/` | Design team sandbox — covers, illustrations, slide decks, the daily dashboard | `sandboxes/design-claude/CLAUDE.md` |
| `sandboxes/va/` | Handoff-team sandbox — files prepared for VA / contractor / freelancer execution | `sandboxes/va/CLAUDE.md` |

> The template ships sandboxes under `sandboxes/`. If you prefer them at root (the original HQ pattern), move them and update this table — see `ARCHITECTURE.md` "Folder layout choice" for the trade-off.

---

## WORKER BRIEFS

`briefs/` — Task contracts for worker sessions. Any worker reads a brief cold and executes without shared history.

| File | What it is |
| --- | --- |
| `briefs/_BRIEF-TEMPLATE.md` | Six-section template — copy, fill slug, dispatch |
| `briefs/EXAMPLE-article-brief.md` | Filled example for a content session |
| `briefs/questions/` | Escalation files — worker writes here when blocked, orchestrator reads next session |

---

## CONTENT STATUS

Operator's per-deliverable tracker (typical filename: `CONTENT-STATUS.md`). All articles, posts, podcasts, books, and design assets with done/posted/missing status. Update whenever something is posted or a new piece is completed.

The template ships without this file — create it when you have your first deliverable. The auto-stamp hook will keep its `Last updated:` line current automatically.

---

## KEY BIOGRAPHICAL FACTS

[Placeholder: your bio facts here. The original sandbox uses this section as a fast lookup for facts that show up frequently in copy — name, years of experience, lineages, founding work, locations. Workers read this when generating bios, About-page copy, or any first-person reference.]

---

Last updated: [date]
