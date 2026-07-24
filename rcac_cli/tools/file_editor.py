# File Editor Tool

"""Utility to apply targeted edits to a file.

Defines an `Edit` dataclass describing a replacement and an `edit_file`
function that applies a list of edits atomically.
"""

import pathlib
import difflib
from dataclasses import dataclass
from typing import List


@dataclass
class Edit:
    start_line: int  # 1‑based inclusive
    end_line: int    # inclusive
    target: str      # exact content to replace (including whitespace)
    replacement: str

def edit_file(path: str, edits: List[Edit]) -> None:
    """Apply a series of non‑overlapping edits to *path*.

    The file is read, each edit is validated against the existing content,
    and the modifications are written back atomically.
    """
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    # Apply edits in reverse order to keep line numbers stable
    for edit in sorted(edits, key=lambda e: e.start_line, reverse=True):
        # Extract existing slice
        start_idx = edit.start_line - 1
        end_idx = edit.end_line
        existing = "".join(lines[start_idx:end_idx])
        if existing != edit.target:
            raise ValueError(
                f"Target mismatch at lines {edit.start_line}-{edit.end_line}.\n"
                f"Expected: {repr(edit.target)}\nGot: {repr(existing)}"
            )
        # Replace slice
        replacement_lines = edit.replacement.splitlines(keepends=True)
        lines[start_idx:end_idx] = replacement_lines
    # Write back
    p.write_text("".join(lines), encoding="utf-8")
