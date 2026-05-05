#!/usr/bin/env python3
"""
Pre-edit snapshot: copy high-blast-radius files to .trash/YYYY-MM-DD/ once per
day before the first edit lands.

Acts as a "git revert without git" floor for the surfaces where a bad edit
ripples (calendar, control files, _config, settings). Per-edit history already
lives in ~/.claude/file-history; this hook adds a discoverable, dated,
project-local restore point at start-of-day granularity.

Protected surfaces (project-relative):
- Root control files: CLAUDE.md, CONTEXT.md, STATUS.md, CONTENT-STATUS.md, *-CALENDAR.md
- _config/* (BRAND.md, REFERENCE.md, _WORKER-RULES.md, etc.)
- .claude/settings.json, .claude/settings.local.json
- Any nested CLAUDE.md / STATUS.md / CONTEXT.md (sandbox control files)
- briefs/_*.md (templates and routine specs — operator-curated)

Logic: on first matching Edit/Write/MultiEdit per day, copy the original to
.trash/YYYY-MM-DD/<flattened-path>. Subsequent edits same day are no-ops
(start-of-day state is what we preserve).

Restore (operator, manual):
  cp .trash/2026-05-05/CLAUDE.md CLAUDE.md
  cp .trash/2026-05-05/_config__BRAND.md _config/BRAND.md

Pruning: weekly maintenance Phase 2 deletes .trash/<date>/ folders >30 days old.

Hook contract: read JSON from stdin, write nothing, exit 0. Failure-safe —
never blocks an edit, even if snapshotting fails.

PROJECT_ROOT is resolved dynamically so this hook works in any clone of the
template: prefer $CLAUDE_PROJECT_DIR (set by Claude Code), fall back to walking
up from this file's location (.claude/hooks/ -> project root).

To disable: rename or remove this file, or comment out the matcher in
.claude/settings.json.
"""

import json
import os
import shutil
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(
    os.environ.get("CLAUDE_PROJECT_DIR")
    or Path(__file__).resolve().parents[2]
)
SANDBOX_CONTROL_NAMES = {"CLAUDE.md", "STATUS.md", "CONTEXT.md"}
ROOT_CONTROL_NAMES = {
    "CLAUDE.md", "CONTEXT.md", "STATUS.md", "CONTENT-STATUS.md",
}


def is_protected(rel_parts: tuple, name: str) -> bool:
    if len(rel_parts) == 1:
        if name in ROOT_CONTROL_NAMES:
            return True
        if name.endswith("-CALENDAR.md"):
            return True
        return False

    if rel_parts[0] == "_config":
        return True

    if (
        rel_parts[0] == ".claude"
        and name.startswith("settings")
        and name.endswith(".json")
    ):
        return True

    if (
        rel_parts[0] == "briefs"
        and name.startswith("_")
        and name.endswith(".md")
    ):
        return True

    if name in SANDBOX_CONTROL_NAMES:
        return True

    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    raw_path = (data.get("tool_input") or {}).get("file_path", "")
    if not raw_path:
        sys.exit(0)

    src = Path(raw_path)
    if not src.exists() or not src.is_file():
        sys.exit(0)

    try:
        rel = src.resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        sys.exit(0)

    if not is_protected(rel.parts, src.name):
        sys.exit(0)

    flattened = str(rel).replace("/", "__")
    today = date.today().isoformat()
    dest = PROJECT_ROOT / ".trash" / today / flattened

    if dest.exists():
        sys.exit(0)

    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
