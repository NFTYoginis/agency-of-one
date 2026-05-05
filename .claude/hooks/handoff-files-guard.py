#!/usr/bin/env python3
"""
Pre-edit guard: prompt before editing handoff-ready files.

Per CLAUDE.md "WHAT NOT TO DO": handoff-ready files (e.g., a build checklist
your VA / contractor / handoff team is executing from) should not be edited
without explicit confirmation. Accidental edits break the contract with whoever
is downstream. This hook surfaces an explicit confirm.

Populate HANDOFF_MARKERS below with path fragments that should trigger the
guard. Each entry can be a folder name, a partial path, or a full filename;
the hook prompts whenever any marker appears anywhere in the edited path.

Examples (replace with the markers that match YOUR handoff surface):
  HANDOFF_MARKERS = (
      "handoff-team/",
      "VA-Build-Checklist.md",
      "spec-pack/",
  )

Leave the tuple empty if you don't have handoff-ready files yet — the hook
becomes a no-op until you populate it.

Hook contract: read JSON from stdin, write JSON to stdout (or nothing), exit 0.
  - No output       -> tool proceeds normally
  - {"decision":"ask", ...}   -> user is prompted (overrides bypass mode)
  - {"decision":"block", ...} -> tool is blocked

To disable: rename or remove this file, or comment out the matcher in
.claude/settings.json.
"""

import json
import sys

# Populate with path fragments that mark your handoff-ready files.
# The hook fires whenever any of these substrings appears in an edited path.
HANDOFF_MARKERS: tuple = (
    # "handoff-team/",
    # "VA-Build-Checklist.md",
    # "spec-pack/",
)


def respond(decision: str, reason: str) -> None:
    print(json.dumps({"decision": decision, "reason": reason}))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    for marker in HANDOFF_MARKERS:
        if marker in file_path:
            respond(
                "ask",
                f"Handoff-ready file: {file_path}\n"
                "Per CLAUDE.md these are downstream contracts. Approve only if "
                "intentionally restructuring the handoff."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
