# Grep Search Tool

"""Utility to perform regex or literal searches across the repository.

Provides `grep_search(query: str, path: str = '.', is_regex: bool = False, case_insensitive: bool = False) -> dict`
which returns a dict with filenames and matching lines.
"""

import pathlib
import re
import subprocess
from typing import List, Dict, Any


def grep_search(query: str, path: str = ".", is_regex: bool = False, case_insensitive: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """Search files under *path* for *query*.

    Returns a mapping of filename to a list of matches, each match is a dict with
    ``line`` (1‑based) and ``content``.
    """
    base = pathlib.Path(path)
    if not base.exists():
        raise FileNotFoundError(f"Search path does not exist: {path}")
    # Build ripgrep command
    cmd = ["rg", "--json"]
    if case_insensitive:
        cmd.append("-i")
    if not is_regex:
        cmd.append("-F")  # fixed string
    cmd.extend([query, str(base)])
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    matches: Dict[str, List[Dict[str, Any]]] = {}
    for line in result.stdout.splitlines():
        try:
            obj = eval(line)  # rg outputs JSON per line; using eval for simplicity
        except Exception:
            continue
        if obj.get("type") != "match":
            continue
        data = obj["data"]
        file_path = data["path"].get("text", "")
        line_num = data["line_number"]
        line_text = data["lines"]["text"]
        matches.setdefault(file_path, []).append({"line": line_num, "content": line_text})
    return matches
