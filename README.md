# RCAC CLI 🚀

An autonomous terminal-based AI coding assistant for RCAC Qwen.

## 🔑 Getting Your RCAC API Key

To get your RCAC API key:
1. Go to [https://genai.rcac.purdue.edu/](https://genai.rcac.purdue.edu/).
2. Click on your profile in the top-right corner.
3. Select **Settings** → **Account** → **API keys**.
4. Copy your API key.

---

## 📦 Quick Installation

### Option 1: Automated Setup (Recommended)
Automatically sets up `.venv`, installs dependencies, and links `rcac` to your system PATH:
```bash
# Clone the repository
git clone https://github.com/AidenBrown21/rcac-cli.git
cd rcac-cli

# Run automated installer
./install.sh
```

### Option 2: Using pipx
```bash
pipx install -e .
```

### Option 3: Manual Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Option 4: Direct Execution
```bash
./rcac
# or
python3 -m rcac_cli.main
```

---

## 🚀 Setup & Usage

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
