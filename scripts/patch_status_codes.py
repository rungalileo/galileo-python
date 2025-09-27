#!/usr/bin/env python3
"""
Patch generated API files to fix missing status codes.

Workflow
--------
1. Find all API endpoint files in the generated directory.
2. For each file, locate lines with 'if response.status_code == :'
3. Replace with proper status codes by extracting from response variable names.
4. Write the file back only if changes were made.

Run this script as a post-generation hook for openapi-python-client.

Exit codes
0 - patches applied successfully
1 - I/O or other error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def fix_status_codes_in_file(file_path: Path) -> bool:
    """Fix missing status codes in a single file. Returns True if changes were made."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Simple approach: find each broken status code check and fix it by looking for context
        lines = content.split("\n")
        modified = False

        for i, line in enumerate(lines):
            if "if response.status_code == :" in line:
                # Look for status code in the next few lines
                status_code = None
                for j in range(i + 1, min(i + 10, len(lines))):
                    # Check for patterns like 'response_200', '_parse_response_200', etc.
                    matches = re.findall(r"(?:response_|_parse_response_|_)(\d{3})", lines[j])
                    if matches:
                        status_code = matches[0]
                        break

                if status_code:
                    lines[i] = line.replace(
                        "if response.status_code == :", f"if response.status_code == {status_code}:"
                    )
                    modified = True

        if modified:
            content = "\n".join(lines)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return False


def fix_status_codes_in_directory(directory: Path) -> int:
    """Fix status codes in all Python files in directory. Returns number of files patched."""
    if not directory.exists():
        print(f"Directory {directory} not found", file=sys.stderr)
        return 0

    patched_count = 0
    python_files = list(directory.rglob("*.py"))

    for file_path in python_files:
        if fix_status_codes_in_file(file_path):
            print(f"Patched {file_path}")
            patched_count += 1

    return patched_count


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <directory_path>", file=sys.stderr)
        return 1

    directory = Path(sys.argv[1])
    patched_count = fix_status_codes_in_directory(directory)

    print(f"Patched {patched_count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
