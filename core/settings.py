import json
import os

CONFIG_PATH = "config.json"

def load_settings():
    if not os.path.exists(CONFIG_PATH):
        return {"stealth_mode": False}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_settings(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def get_settings_summary(config=None):
    if config is None:
        config = load_settings()

    stealth = "Enabled" if config.get("stealth_mode") else "Disabled"

    return f"""
    Current Settings
    ----------------
    Stealth Mode: {stealth}
    """
