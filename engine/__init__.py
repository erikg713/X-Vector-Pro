import os
import json
import importlib
from datetime import datetime
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
EXPLOITS_DIR = os.path.join(os.path.dirname(__file__), "exploits")
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(category, data):
    """
    Log a structured event to a JSON log file.

    Args:
        category (str): e.g. "scan", "recon", "brute", "exploit"
        data (dict): Your scan result, brute result, etc.
    """
    # Replace ":" with "-" in the timestamp to make it filename-safe
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{category}_{timestamp}.json")

    log_data = {
        "timestamp": timestamp,
        "category": category,
        "data": data
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    return log_file

# Auto-discover exploit modules
def discover_exploits():
    exploit_modules = []
    for file in os.listdir(EXPLOITS_DIR):
        if file.endswith(".py") and file != "__init__.py":
            mod_name = file[:-3]
            try:
                mod = importlib.import_module(mod_name)
                exploit_modules.append((mod_name, mod))
                print(f"[+] Loaded exploit module: {mod_name}")
            except Exception as e:
                print(f"[!] Failed to load exploit {mod_name}: {e}")
def initialize_environment():
    # Initialize necessary environment settings
    pass

# Initialize everything
initialize_environment()
discovered_exploits = discover_exploits()
initialize_environment()
discovered_exploits = discover_exploits()
