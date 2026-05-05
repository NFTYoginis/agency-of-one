#!/usr/bin/env python3
"""
Pre-tool-use safety hook for Claude Code.

Forces a user prompt for the two highest-risk Bash command patterns:
  1. rm -rf — any flag combination of recursive + force
  2. git push --force / -f — any force-push variant

Everything else passes through silently, so bypassPermissions mode stays fast.

Hook contract: read JSON from stdin, write JSON to stdout (or nothing), exit 0.
  - No output / empty output  -> tool proceeds normally
  - {"decision":"ask",   ...} -> user is prompted (overrides bypass mode)
  - {"decision":"block", ...} -> tool is blocked entirely; reason shown to model
  - {"decision":"approve", ...} -> tool runs without any prompt (we don't use this)

To temporarily disable this hook, comment out the hooks block in
.claude/settings.json or rename this file. Re-enable by reverting.
"""

import json
import re
import shlex
import sys


def respond(decision: str, reason: str) -> None:
    print(json.dumps({"decision": decision, "reason": reason}))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Malformed input — fail open, let the tool through
        sys.exit(0)

    # Only inspect Bash tool calls
    if data.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = ((data.get("tool_input") or {}).get("command") or "").strip()
    if not cmd:
        sys.exit(0)

    # Detect rm -rf in any flag combination
    # Catches: rm -rf, rm -fr, rm -Rf, rm -fR, rm -rfv, rm -vrf,
    #          rm -r -f, rm -f -r, rm --recursive --force, etc.
    if re.search(r"(?:^|[\s;&|`])rm\b", cmd):
        try:
            tokens = shlex.split(cmd, posix=True)
        except ValueError:
            # Unbalanced quotes — fail open
            sys.exit(0)

        for i, tok in enumerate(tokens):
            if tok != "rm":
                continue
            short_flags = ""
            long_flags = []
            for nxt in tokens[i + 1:]:
                if nxt.startswith("--"):
                    long_flags.append(nxt)
                elif nxt.startswith("-") and len(nxt) > 1:
                    short_flags += nxt[1:]
                else:
                    break
            has_r = "r" in short_flags or "R" in short_flags or "--recursive" in long_flags
            has_f = "f" in short_flags or "--force" in long_flags
            if has_r and has_f:
                respond(
                    "ask",
                    "Safety hook: rm with both -r and -f flags detected. "
                    "Approve ONLY if the path is correct. "
                    "Safer alternative: `mv FILE ~/.Trash/` (recoverable)."
                )
            break

    # Detect git push --force / -f
    if re.search(r"\bgit\s+push\b", cmd):
        if re.search(
            r"(?:\s|^)(?:-f|--force(?:-with-lease|-if-includes)?)\b",
            cmd,
        ):
            respond(
                "ask",
                "Safety hook: git push with --force / -f detected. "
                "Approve ONLY if rewriting remote history is intentional."
            )

    # All other commands pass through silently
    sys.exit(0)


if __name__ == "__main__":
    main()
