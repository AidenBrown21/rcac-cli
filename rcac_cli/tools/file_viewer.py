# File Viewer Tool

"""Utility to read a portion of a file.

Provides `view_file(path: str, start: int = 1, end: int | None = None) -> str`
which returns the selected lines (inclusive). If `end` is None the rest
of the file is returned.
"""

import pathlib
from typing import Optional


def view_file(path: str, start: int = 1, end: Optional[int] = None) -> str:
    """Return the contents of *path* from line *start* to *end* (1‑based).

    Args:
        path: Path to the file.
        start: First line to include (default 1).
        end: Last line to include (inclusive). If omitted, reads to EOF.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If *start* is less than 1 or *end* is before *start*.
    """
    if start < 1:
        raise ValueError("start must be >= 1")
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    lines = p.read_text(encoding="utf-8").splitlines()
    # Convert to 0‑based indices
    start_idx = start - 1
    end_idx = end if end is None else end
    if end_idx is not None and end_idx < start:
        raise ValueError("end must be >= start")
    selected = lines[start_idx:end_idx]
    return "\n".join(selected)
