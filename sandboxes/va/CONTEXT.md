# va — Context

Handoff-team environment. Read this after CLAUDE.md.

---

## Current priorities

[Placeholder: what's currently being built for handoff. Example structure: "Active build pack: <project>. Phase 3 of 5. VA last delivered punch-list response on [date]. Next gate: operator review of [item]."]

_No active build packs — awaiting first orchestrator dispatch._

---

## Reference Exemplars

Build packs are domain-specific — the canonical example is whichever pack last shipped successfully. Until you've shipped one, this table stays empty.

| Format | Canonical exemplar | What it demonstrates |
| --- | --- | --- |
| Build brief (HTML) | _TBD_ | [Placeholder: structure — context, scope, asset map, per-page table, FAQ for the VA] |
| Page-specs sheet | _TBD_ | [Placeholder: per-page row format — slug, title, meta, OG image, CTA, dependencies] |
| Build checklist | _TBD_ | [Placeholder: phase shape — goal, dependency-ordered items, exit criteria] |
| Punch list | _TBD_ | [Placeholder: round-N format — issue, page reference, fix, severity, blocker?] |

---

## What to load per task

| Task | Load first | Then load |
| --- | --- | --- |
| Draft a new build brief | Active calendar / project plan that drives the handoff | Source files this build draws from (content sandbox MDs, design sandbox PNGs, OG images) |
| Update page-specs after design lands | The most recent page-specs file in `[project]/` | The list of assets that just shipped (from `STATUS.md` or the orchestrator's dispatch) |
| Write punch-list entry | The current build pack | The VA's most recent delivery (URL or screenshot the operator passed back) |

---

## Default Inputs (Layer 3 / Layer 4)

| Layer | File | Why |
| --- | --- | --- |
| 3 | `../_config/BRAND.md` | voice + visual rules referenced in build briefs |
| 3 | `../_config/REFERENCE.md` | brand tokens, file naming, locked phrases |
| 3 | `../_config/RELATED_PROJECTS.md` | if the build is on a related property, the relationship rules live here |
| 4 | active build pack files | named in each brief's Inputs table |
| 4 | source asset list | from the orchestrator's dispatch — usually a path list, not a file |

Workers do not load files outside this list speculatively. If a brief requires more, the brief's Inputs table names them.
