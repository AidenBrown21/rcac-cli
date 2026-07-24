import os
import subprocess
import json
from typing import Dict, Any, List

# Import concrete tool implementations
from rcac_cli.tools.file_viewer import view_file as tool_view_file
from rcac_cli.tools.file_editor import edit_file as tool_edit_file, Edit as FileEdit
from rcac_cli.tools.grep_search import grep_search as tool_grep_search
from rcac_cli.tools.terminal_executor import execute_command as tool_execute_command
from rcac_cli.context.repo_map import build_repo_map as tool_build_repo_map

# Unified tool schema used by the REPL
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists files in a given directory.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Directory path (default '.')"}}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "File path"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write/overwrite a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Full file content"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and capture output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Command to run"}},
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_file",
            "description": "Read a range of lines from a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "start": {"type": "integer", "description": "Start line (1‑based)"},
                    "end": {"type": "integer", "description": "End line (inclusive)"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Apply targeted non‑overlapping edits to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "edits": {
                        "type": "array",
                        "description": "List of edit specifications",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start_line": {"type": "integer"},
                                "end_line": {"type": "integer"},
                                "target": {"type": "string"},
                                "replacement": {"type": "string"}
                            },
                            "required": ["start_line", "end_line", "target", "replacement"]
                        }
                    }
                },
                "required": ["path", "edits"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grep_search",
            "description": "Search for a pattern across files using ripgrep.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search pattern"},
                    "path": {"type": "string", "description": "Root directory (default '.'"},
                    "is_regex": {"type": "boolean", "description": "Treat query as regex"},
                    "case_insensitive": {"type": "boolean", "description": "Case‑insensitive"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Run a shell command synchronously and capture output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "array", "items": {"type": "string"}, "description": "Command + args"},
                    "cwd": {"type": "string", "description": "Working directory"},
                    "capture_output": {"type": "boolean", "description": "Capture stdout/stderr"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_repo_map",
            "description": "Create a lightweight repository map of Python classes and functions.",
            "parameters": {
                "type": "object",
                "properties": {"root": {"type": "string", "description": "Repository root"}},
                "required": []
            }
        }
    }
]

def execute_tool(name: str, arguments: dict) -> str:
    """Dispatch tool calls to concrete implementations."""
    try:
        if name == "list_directory":
            path = arguments.get("path", ".")
            return str(os.listdir(path))
        if name == "read_file":
            with open(arguments["path"], "r", encoding="utf-8") as f:
                return f.read()
        if name == "write_file":
            with open(arguments["path"], "w", encoding="utf-8") as f:
                f.write(arguments["content"])
            return "File written successfully."
        if name == "run_command":
            result = subprocess.run(
                arguments["command"],
                cwd=arguments.get("cwd", "."),
                capture_output=arguments.get("capture_output", True),
                text=True,
                stdin=subprocess.DEVNULL,
                timeout=120,
                check=False,
            )
            out = result.stdout
            if result.stderr:
                out += "\nSTDERR:\n" + result.stderr
            return out if out.strip() else "Command executed successfully with no output."
        if name == "view_file":
            return tool_view_file(arguments["path"], arguments.get("start", 1), arguments.get("end"))
        if name == "edit_file":
            edits = [FileEdit(**e) for e in arguments["edits"]]
            tool_edit_file(arguments["path"], edits)
            return "File edited successfully."
        if name == "grep_search":
            return json.dumps(tool_grep_search(
                arguments["query"],
                arguments.get("path", "."),
                arguments.get("is_regex", False),
                arguments.get("case_insensitive", False),
            ))
        if name == "execute_command":
            return tool_execute_command(
                arguments["command"],
                arguments.get("cwd", "."),
                arguments.get("capture_output", True),
            )
        if name == "build_repo_map":
            return json.dumps(tool_build_repo_map(arguments.get("root", ".")))
        return f"Error: Unknown tool {name}"
    except Exception as e:
        return f"Error executing {name}: {str(e)}"
