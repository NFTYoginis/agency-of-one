# [Your brand] — Session Context

Read this after CLAUDE.md. Tells you who you're working with, what's active, and what to load per task. Don't load anything else until you know which task you're doing.

---

## Who You're Working With

[Placeholder: who you're working with — name, role, years of experience, primary properties / brands. Example structure: "[Founder Name] — [role] ([N] years, since [year]), [other roles]. Brand owner: [property A] · [property B] · [property C]. Based: [location]."]

Voice: [Placeholder: 3–4 adjectives that anchor the brand voice. See `_config/BRAND.md` § 3 for the full say/don't-say table.]

[Placeholder: your three (or N) pillars — copy from `_config/BRAND.md` § 5 once filled in.]

---

## What's Active Right Now

| Priority | Item | Status |
| --- | --- | --- |
| 1 | [Placeholder: top current priority] | [Placeholder: status note] |
| 2 | [Placeholder: priority 2] | [Placeholder] |
| 3 | [Placeholder: priority 3] | [Placeholder] |

> Operator: refresh this table at the start of each month, or whenever an active thread changes shape. Stale priorities here will mislead future sessions — when a priority lands or drops, update the row.

---

## What to Load for Each Task Type

> **Skip column is load-bearing.** Read it. The default failure mode is reading "just-in-case" files; the Skip column makes that an explicit rule violation, not a judgment call.

| Task | Load first | Then load | Skip |
| --- | --- | --- | --- |
| Daily execution (routine) | Calendar row (grep one row) | — | Yesterday's MD/HTML, source files, full week section, REFERENCE.md, full template |
| Write an article | Sandbox content guide / brief | Brief in `content-claude/articles/briefs/` | Design docs, calendar, daily briefs, `_config/REFERENCE.md` design specs |
| Write social post | `content-claude/CLAUDE.md` | Topic brief or platform-specific guide | Full article briefs, design docs, weekly strategy, prior daily briefs |
| Write podcast / long-form script | `content-claude/CLAUDE.md` | `content-claude/podcast/CLAUDE.md` (or equivalent) | Design docs, calendar, social specs |
| Design — slides / thumbnail / story | `design-claude/CLAUDE.md` | Article brief in `design-claude/articles/briefs/` | Writing voice docs, full article body, calendar |
| Design — reel covers | `design-claude/CLAUDE.md` | `design-claude/scripts/generate_cover.js` (or equivalent) | Writing voice docs, full article body, podcast docs |
| Design — book / long-form cover | `design-claude/CLAUDE.md` | Brief in `design-claude/Book Cover/[Title]/` | Calendar, daily briefs, social specs |
| Design — illustrations / diagrams | `design-claude/CLAUDE.md` | Brief in `design-claude/illustrations/briefs/` | Writing voice docs, calendar, daily briefs |
| Handoff-team build | Memory: `project_handoff_build` (if you've created one) | `va/handoff-checklist.md` (or equivalent) | Content sandboxes, calendar, daily briefs |
| Brand strategy | `_config/BRAND.md` | Whatever the brand-strategy file points to | Per-task working files |

---

## Funnel Architecture (quick ref)

[Placeholder: your funnel architecture — sketch the conversion map from cold lead to repeat customer. The original sandbox uses an ASCII diagram; you can use bullets, a table, or a diagram link. The point is a fast reference workers can grep when writing copy that lives somewhere on the funnel.]

```text
[Placeholder: e.g.]
Free opt-in
→ first-purchase trigger
  YES -> sequence A (onboarding) -> sequence B (depth) -> sequence C (premium)
  NO  -> sequence D (re-engagement) -> sequence E (last-chance)
-> Premium product -> sequence F -> renewal/loyalty
```

---

## Dispatching a Worker Session

1. Copy `briefs/_BRIEF-TEMPLATE.md` → save as `briefs/<slug>.md`
2. Fill: worker, sandbox entry point, task, context paths, scope, binary acceptance, returns-with
3. Open the sandbox in a fresh session and hand it the brief
4. If the worker gets stuck, it writes to `briefs/questions/<slug>-question.md` — read it next session

Cold-start rule: if the brief cannot stand alone without this chat history, it is not finished.

---

## Working Style Notes

- When writing in the brand voice, read `_config/BRAND.md` voice rules + `_config/REFERENCE.md` key phrases first
- Design work: follow the brand rules in `_config/BRAND.md` § 6 and the spec table in `_config/REFERENCE.md`
- Per-deliverable tracker updates only after operator confirms a piece is live
- Cross-cutting boundary / escalation rules: `_config/_WORKER-RULES.md`

(Operator triggers and "what not to do" rules live in CLAUDE.md — don't duplicate here.)
