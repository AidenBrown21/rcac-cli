import os
import ast
from typing import List, Dict

def _parse_python_file(path: str) -> Dict[str, List[str]]:
    """Parse a Python file and return its classes and functions signatures."""
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source, filename=path)
    classes = []
    functions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            sig = f"{node.name}({', '.join(args)})"
            functions.append(sig)
    return {"classes": classes, "functions": functions}

def build_repo_map(root: str) -> Dict[str, Dict]:
    """Walk the repository starting at *root* and build a map of files to their symbols.

    Returns a dict where keys are file paths (relative to root) and values contain
    ``"classes"`` and ``"functions"`` lists.
    """
    repo_map = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.py'):
                full_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(full_path, root)
                repo_map[rel_path] = _parse_python_file(full_path)
    return repo_map

def search_repo_map(repo_map: Dict[str, Dict], query: str) -> List[str]:
    """Simple search for *query* in class or function names.
    Returns a list of matching file paths.
    """
    matches = []
    for path, symbols in repo_map.items():
        if any(query in name for name in symbols.get('classes', [])):
            matches.append(path)
        elif any(query in func for func in symbols.get('functions', [])):
            matches.append(path)
    return matches
