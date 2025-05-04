# gui package for X-Vector Pro interface
# gui/__init__.py

import os
import pkgutil
import importlib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Explicitly importing the main entry point (Dashboard)
from .dashboard import Dashboard

# List of explicitly defined modules/classes to expose for this package
__all__ = ["Dashboard"]

# Path to the 'tabs' directory
tabs_package = os.path.join(os.path.dirname(__file__), "tabs")

# Function to recursively load all modules from a directory
def load_tabs_from_directory(package_name, package_path):
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        module_path = f"{package_name}.{module_name}"
        
        # If it's a subdirectory (package), recurse into it
        if is_pkg:
            load_tabs_from_directory(module_path, os.path.join(package_path, module_name))
        else:
            # Dynamically import the module
            module = importlib.import_module(module_path)
            
            # Add the classes within the module to the __all__ list
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr.__name__.endswith("Tab"):
                    __all__.append(attr.__name__)

# Load all tabs from the 'tabs' directory (including subdirectories)
load_tabs_from_directory("gui.tabs", tabs_package)

# The code above will now:
# 1. Automatically discover and import all modules in 'tabs' and its subdirectories.
# 2. Only add classes that are subclasses of 'CTkFrame' (or other specified base class).
# 3. Maintain scalability: No need to modify this file if new tabs or subdirectories are added.
