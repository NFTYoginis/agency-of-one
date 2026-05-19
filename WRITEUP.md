# WRITEUP

**What was built.** A Claude Code template for running a content/design business as a solo operator. One orchestrator session plus several worker sandboxes (`content-claude` / `design-claude` / `research-claude` / `va`), with task dispatch via brief files instead of chat history. Ships with the folder tree, brief templates, four Python hooks (safety-check · snapshot-before-edit · auto-stamp-date · handoff-files-guard), two skills, and one canonical example brief — ready to populate with brand-specific content.

**The design decision worth surfacing.** Folder structure is the agent architecture. The Interpretable Context Methodology (ICM) layers (L0–L4) separate orchestrator logic from worker sandboxes; briefs work as cold-start handoff contracts so a worker can execute without prior chat history; `STATUS.md` breadcrumbs replace the operator-as-message-bus pattern. The shape is domain-agnostic — the README states "the shape would be different for a different domain; the underlying pattern is the same."

**What's next.** The README defines the template only. A private full version (with brand-voice machinery, multi-channel calendar automation, video animation pipelines, and book-publishing workflows) is offered as custom consulting, not as a public feature addition. The public template is intentionally the scaffold, not the populated business.
