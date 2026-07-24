#!/usr/bin/env bash
set -e

echo "🚀 Installing RCAC CLI..."

# Detect Python 3
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "❌ Error: Python 3 is required but was not found."
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    "$PYTHON_BIN" -m venv .venv
fi

# Install dependencies into .venv
echo "📥 Installing dependencies..."
.venv/bin/pip install -q -e .

# Create symlink in user bin directory (~/.local/bin)
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ln -sf "$SCRIPT_DIR/.venv/bin/rcac" "$BIN_DIR/rcac"

# Check if ~/.local/bin is in PATH, prompt/add to shell profile if missing
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    if [ -n "$SHELL_PROFILE" ] && [ -f "$SHELL_PROFILE" ]; then
        if ! grep -q '\.local/bin' "$SHELL_PROFILE"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_PROFILE"
            echo "✅ Added $BIN_DIR to $SHELL_PROFILE"
        fi
    fi
fi

echo ""
echo "✅ Installation complete!"
echo "🎉 You can now run 'rcac' from any terminal directory."
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "💡 Note: Please restart your terminal or run: source $SHELL_PROFILE"
fi
