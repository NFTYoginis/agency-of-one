#!/usr/bin/env python3
"""
Post-edit hook: auto-stamp the "Last updated:" line in CONTENT-STATUS.md.

Saves one Edit call per content update — the date line never goes stale,
the orchestrator never has to remember to bump it.

Hook contract: read JSON from stdin, write nothing, exit 0. Side effect is
the file edit itself (not visible in tool output, but verifiable on next read).

To disable: rename or remove this file, or comment out the matcher in
.claude/settings.json.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path.endswith("CONTENT-STATUS.md"):
        sys.exit(0)

    p = Path(file_path)
    if not p.exists():
        sys.exit(0)

    today = date.today()
    human_date = f"{MONTH_NAMES[today.month]} {today.day}, {today.year}"

    text = p.read_text()
    new_text, n = re.subn(
        r"^(Last updated:) [^.\n]+\.",
        rf"\1 {human_date}.",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    if n and new_text != text:
        p.write_text(new_text)

    sys.exit(0)


if __name__ == "__main__":
    main()
