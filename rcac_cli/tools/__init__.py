# Tools package initializer

"""Exports for tool utilities used by the REPL infrastructure.

The individual modules provide file viewing, editing, searching and command execution.
"""

from .file_viewer import view_file
from .file_editor import edit_file, Edit
from .grep_search import grep_search
# Avoid circular import; TOOLS_SCHEMA imported directly where needed

# NOTE: REPL‑level utilities are imported directly from the top‑level `rcac_cli.tools` module.
# This avoids a circular import between the package `rcac_cli.tools` and the module `rcac_cli.tools`.
