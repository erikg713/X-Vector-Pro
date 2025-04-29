"""
X-Vector Pro - Engine Core Initializer

Initializes engine environment, async utilities, and dynamic module loading.
Auto-discovers exploits and prepares global access to engine resources.
"""

import os
import sys
import threading
import importlib
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
CORE_MODULES_DIR = BASE_DIR / "core"
EXPLOITS_DIR = BASE_DIR / "exploits"
WORDLISTS_DIR = BASE_DIR / "wordlists"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

# Ensure required directories exist
def initialize_environment():
    for directory in [EXPLOITS_DIR, WORDLISTS_DIR, REPORTS_DIR, LOGS_DIR]:
        os.makedirs(directory, exist_ok=True)
    if str(CORE_MODULES_DIR) not in sys.path:
        sys.path.insert(0, str(CORE_MODULES_DIR))
    if str(EXPLOITS_DIR) not in sys.path:
        sys.path.insert(0, str(EXPLOITS_DIR))

# Thread utility
THREAD_POOL = []

def run_async(func, *args, **kwargs):
    """Run a function in a background thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    THREAD_POOL.append(thread)
    thread.start()
    return thread

# Module loader
def load_module_by_name(name):
    """Dynamically load a core or exploit module by name."""
    try:
        return importlib.import_module(name)
    except ImportError as e:
        print(f"[!] Failed to load module '{name}': {e}")
        return None

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
    return exploit_modules

# Initialize everything
initialize_environment()
discovered_exploits = discover_exploits()
