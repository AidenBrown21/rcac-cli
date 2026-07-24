# Git utilities for workflow rollback

"""Helper functions to manage a temporary Git branch for safe operations.

- create_temp_branch(): creates and checks out a new branch named
  `rcac-repl-work` (or a unique name if it exists).
- rollback_to_original(): checks out the original branch and deletes the temp branch.
"""

import subprocess
import os
from typing import Optional

def _run_git(args: list[str], cwd: Optional[str] = None) -> str:
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout.strip()

def create_temp_branch(branch_name: str = "rcac-repl-work") -> str:
    """Create and checkout a temporary branch.

    Returns the name of the branch that was checked out.
    """
    # Determine current branch
    current = _run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    # Ensure branch name is unique
    existing = _run_git(["branch", "--list", branch_name])
    if existing:
        # Append a suffix to make it unique
        i = 1
        while _run_git(["branch", "--list", f"{branch_name}-{i}"]):
            i += 1
        branch_name = f"{branch_name}-{i}"
    # Create and checkout new branch
    _run_git(["checkout", "-b", branch_name])
    return branch_name

def rollback_to_original(original_branch: str) -> None:
    """Checkout the original branch and delete the temporary one.
    """
    # Get current branch (temp)
    temp_branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    # Checkout original branch
    _run_git(["checkout", original_branch])
    # Delete temp branch
    _run_git(["branch", "-D", temp_branch])
