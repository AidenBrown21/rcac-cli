# RCAC CLI 🚀

An autonomous terminal-based AI coding assistant for RCAC Qwen.

## 📦 Quick Installation

You can install `rcac-cli` directly using `pip` or `pipx`:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/rcac-cli.git
cd rcac-cli

# Install locally in editable mode (or via pipx)
pip install -e .
```

---

## 🔑 Setup & Usage

### 1. Interactive First-Run Prompt
Simply type `rcac` in your terminal:

```bash
rcac
```

If no API key is detected, the CLI will automatically prompt you:

```text
🔑 RCAC API Key required.
Please enter your RCAC API Key: <PASTE_YOUR_API_KEY_HERE>
✅ API Key saved to ~/.rcac/config.json
```

Once entered, your API key will be safely stored in `~/.rcac/config.json`.

---

### 2. Manual API Key Setup
You can also set or update your API key anytime via the command line:

```bash
rcac set-key "your-api-key-here"
```

Or by setting an environment variable:

```bash
export RCAC_API_KEY="your-api-key-here"
```

---

## 🛠 Features

- **Continuous REPL Loop**: Interactive terminal interface.
- **Autonomous Tool Calling**: Reads files, applies targeted code edits, searches directories, and executes terminal commands automatically.
- **Local Config Management**: API keys stored in your home directory (`~/.rcac/config.json`), keeping your repository clean and shareable.
