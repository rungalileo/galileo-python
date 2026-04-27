#!/usr/bin/env python3
"""
Patch the generated HTTPValidationError model so it correctly handles both
list-of-ValidationError and plain-string ``detail`` payloads from the API.

Some API error paths (e.g. invalid model alias) return a 422 whose ``detail``
is a plain string instead of the standard list-of-ValidationError objects.
The auto-generated ``from_dict`` iterates ``detail`` unconditionally, which
causes it to crash when ``detail`` is a string (each character is passed to
``ValidationError.from_dict``).  This script fixes that by replacing the
generated for-loop with an isinstance-guarded block, and changes the field
initialisation from an empty list to UNSET so missing/absent detail is
distinguishable from an empty error list.

Workflow
--------
Run this script as a post-generation hook after
``scripts/auto-generate-api-client.sh``::

    python scripts/patch_http_validation_error.py \\
        src/galileo/resources/models/http_validation_error.py

Exit codes
----------
0  patch applied successfully
1  I/O or syntax error
2  expected pattern not found in target (template drift — update this script)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns to find in the auto-generated file
# ---------------------------------------------------------------------------

# Inside from_dict — bare initialisation + for-loop produced by the generator:
#
#     detail = []
#     _detail = d.pop("detail", UNSET)
#     for detail_item_data in _detail or []:
#         detail_item = ValidationError.from_dict(detail_item_data)
#                                                                      <- blank line
#         detail.append(detail_item)
#
# The class-level field annotation already comes out as
# `Union[Unset, list["ValidationError"]] = UNSET` from the generator, so it
# does NOT need to be patched — only the from_dict body is rewritten here.
_LOOP_RE = re.compile(
    r"(?P<indent>[ \t]+)detail = \[\]\n"
    r"(?P=indent)_detail = d\.pop\(\"detail\", UNSET\)\n"
    r"(?P=indent)for detail_item_data in _detail or \[\]:\n"
    r"(?P=indent)    detail_item = ValidationError\.from_dict\(detail_item_data\)\n"
    r"[ \t]*\n"
    r"(?P=indent)    detail\.append\(detail_item\)",
    re.MULTILINE,
)


def _loop_replacement(indent: str) -> str:
    i = indent
    i4 = indent + "    "
    return "\n".join(
        [
            f"{i}detail: Union[Unset, list[ValidationError]] = UNSET",
            f'{i}_detail = d.pop("detail", UNSET)',
            f"{i}if isinstance(_detail, list):",
            f"{i4}detail = [ValidationError.from_dict(item) for item in _detail]",
            f"{i}elif isinstance(_detail, str) and _detail:",
            f"{i4}# Some backend 422s return a bare string instead of the standard",
            f"{i4}# list-of-ValidationError shape (e.g. invalid model alias lookups",
            f'{i4}# returning {{"detail": "Model alias \'...\' not found"}}).',
            f"{i4}# Wrap it so callers always receive a consistent ValidationError list.",
            f'{i4}detail = [ValidationError(loc=[], msg=_detail, type_="server_error")]',
        ]
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


_PATCHED_SENTINEL = "isinstance(_detail, list)"


def patch(text: str) -> tuple[str, bool]:
    """Rewrite the from_dict loop; return (patched_text, success)."""
    patched, count = _LOOP_RE.subn(lambda m: _loop_replacement(m.group("indent")), text)
    # Treat the file as already-patched if no replacements were made but the
    # patched sentinel is present — ensures idempotent re-runs exit 0 instead
    # of falsely reporting template drift (exit 2).
    already_patched = count == 0 and _PATCHED_SENTINEL in text
    return patched, bool(count) or already_patched


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <file_path>", file=sys.stderr)
        return 1

    target = Path(sys.argv[1])

    try:
        original = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"{target} not found", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Error reading {target}: {e}", file=sys.stderr)
        return 1

    patched, success = patch(original)

    if not success:
        print(
            f"Expected patterns not found in {target} — template may have changed. "
            "Update this script to match the new generated code.",
            file=sys.stderr,
        )
        return 2

    if patched == original:
        print(f"{target} already patched — nothing to do.")
        return 0

    try:
        target.write_text(patched, encoding="utf-8")
    except OSError as e:
        print(f"Error writing {target}: {e}", file=sys.stderr)
        return 1

    print(f"Patched {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
