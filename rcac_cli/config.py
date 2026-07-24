import json
import os
from pathlib import Path

# Use temporary directory during automated tests to avoid touching user's real config
if "PYTEST_CURRENT_TEST" in os.environ:
    CONFIG_DIR = Path("/tmp/.rcac_test")
else:
    CONFIG_DIR = Path.home() / ".rcac"

CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "api_key": "",
    "base_url": "https://genai.rcac.purdue.edu",
    "endpoint": "/api/chat/completions",
    "model": "qwen3.6:27b"
}

def load_config():
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                saved = json.load(f)
                cfg.update(saved)
        except Exception:
            pass
    # Environment variable override takes precedence
    env_key = os.getenv("RCAC_API_KEY")
    if env_key:
        cfg["api_key"] = env_key
    return cfg

def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def set_api_key(key: str):
    cfg = load_config()
    cfg["api_key"] = key.strip()
    save_config(cfg)

def ensure_api_key():
    """Prompts user for API key if missing/placeholder and saves it locally."""
    cfg = load_config()
    current_key = cfg.get("api_key", "").strip()
    
    # Prompt if empty or if invalid dummy key was saved (e.g. 'exit')
    if not current_key or current_key.lower() in {'exit', 'quit', 'none', 'null'}:
        print("🔑 RCAC API Key required.")
        key = input("Please enter your RCAC API Key: ").strip()
        if key:
            set_api_key(key)
            print("✅ API Key saved to ~/.rcac/config.json\n")
            cfg["api_key"] = key
        else:
            print("⚠️ Warning: No API key provided.\n")
    return cfg
