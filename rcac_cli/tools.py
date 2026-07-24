import os
import subprocess
import json
from typing import Dict, Any, List

# Import new tool implementations
from rcac_cli.tools.file_viewer import view_file as tool_view_file
from rcac_cli.tools.file_editor import edit_file as tool_edit_file, Edit as FileEdit
from rcac_cli.tools.grep_search import grep_search as tool_grep_search
from rcac_cli.tools.terminal_executor import execute_command as tool_execute_command
from rcac_cli.context.repo_map import build_repo_map as tool_build_repo_map

# Existing schema definitions for basic file operations
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists files in a given directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the directory to list. Default is current directory."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a specified file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes or overwrites a file with new content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to write."
                    },
                    "content": {
                        "type": "string",
                        "description": "The full content to write to the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Executes a bash command and returns the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The bash command to execute."
                    }
                },
                "required": ["command"]
            }
        }
    },
    # New tool schemas
    {
        "type": "function",
        "function": {
            "name": "view_file",
            "description": "Read a range of lines from a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "start": {"type": "integer", "description": "Starting line (1-based)"},
                    "end": {"type": "integer", "description": "Ending line (inclusive)"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Apply targeted edits to a file using non-overlapping line ranges.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "edits": {
                        "type": "array",
                        "description": "List of edit objects",
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
                    "path": {"type": "string", "description": "Root directory (default .)"},
                    "is_regex": {"type": "boolean", "description": "Treat query as regex"},
                    "case_insensitive": {"type": "boolean", "description": "Case-insensitive search"}
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
                    "command": {"type": "array", "items": {"type": "string"}, "description": "Command and arguments"},
                    "cwd": {"type": "string", "description": "Working directory"},
                    "capture_output": {"type": "boolean", "description": "Whether to capture output"}
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
                "properties": {
                    "root": {"type": "string", "description": "Root directory of the repository"}
                },
                "required": []
            }
        }
    }
]

def execute_tool(name: str, arguments: dict) -> str:
    """Dispatch the tool call to the appropriate implementation."""
    try:
        if name == "list_directory":
            path = arguments.get("path", ".")
            return str(os.listdir(path))
        elif name == "read_file":
            with open(arguments["path"], "r", encoding="utf-8") as f:
                return f.read()
        elif name == "write_file":
            with open(arguments["path"], "w", encoding="utf-8") as f:
                f.write(arguments["content"])
            return "File written successfully."
        elif name == "run_command":
                    capture_output=True,
                    stdin=subprocess.DEVNULL,
                    timeout=120
                )
                output = result.stdout
                if result.stderr:
                    output += "\nSTDERR:\n" + result.stderr
                return output if output.strip() else "Command executed successfully with no output."
            except subprocess.TimeoutExpired:
                return "Error: Command timed out after 120 seconds. Did you run a command that waits for interactive user input? The environment is non-interactive."
        else:
            return f"Error: Unknown tool {name}"
    except Exception as e:
        return f"Error executing {name}: {str(e)}"
