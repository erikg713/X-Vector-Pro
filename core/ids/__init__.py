# core/ids/__init__.py

"""
Intrusion Detection System (IDS) Package Initialization

This module initializes and registers all available IDS strategies.
Each IDS module should define a `run_detection(target)` function.
"""

import os
import importlib

IDS_MODULES = {}

def load_ids_modules():
    ids_dir = os.path.dirname(__file__)
    for file in os.listdir(ids_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            try:
                module = importlib.import_module(f"core.ids.{module_name}")
                if hasattr(module, "run_detection"):
                    IDS_MODULES[module_name] = module.run_detection
            except Exception as e:
                print(f"[IDS Loader] Failed to load {module_name}: {e}")

def run_all_ids(target):
    results = {}
    for name, run_func in IDS_MODULES.items():
        try:
            results[name] = run_func(target)
        except Exception as e:
            results[name] = f"Error: {e}"
    return results

# Load IDS modules at package import
load_ids_modules()
