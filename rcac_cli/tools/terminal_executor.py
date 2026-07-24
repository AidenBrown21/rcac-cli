# Terminal Executor Tool

"""Utility to run shell commands synchronously and capture output.

Provides `execute_command(command: List[str], cwd: str = ".", capture_output: bool = True) -> str`
which runs the command, raising on non‑zero exit codes.
"""

import subprocess
import os
from typing import List


def execute_command(command: List[str], cwd: str = ".", capture_output: bool = True) -> str:
    """Execute *command* in *cwd*.

    Args:
        command: List of command arguments (e.g., ["git", "status"]).
        cwd: Directory to execute in.
        capture_output: If True, returns stdout + stderr; otherwise prints.
    Returns:
        Captured output string.
    Raises:
        subprocess.CalledProcessError if the command exits with a non‑zero status.
    """
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture_output,
        check=False,
        stdin=subprocess.DEVNULL,
        timeout=300,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, command, output=result.stdout, stderr=result.stderr
        )
    output = result.stdout
    if result.stderr:
        output += "\nSTDERR:\n" + result.stderr
    return output if output.strip() else "Command executed successfully with no output."
