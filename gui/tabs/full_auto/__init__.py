"""
This module initializes the `full_auto` functionality for the GUI tool.

It provides:
- The `run_auto_recon` function for automatic reconnaissance tasks.
- The `FullAutoTab` class for integrating the full-auto UI tab into the application.
"""

# Import necessary components with error handling
try:
    from .auto_recon import run_auto_recon
except ImportError as e:
    raise ImportError("Failed to import `run_auto_recon` from auto_recon module.") from e

try:
    from gui.tabs.full_auto import FullAutoTab
except ImportError as e:
    raise ImportError("Failed to import `FullAutoTab` from gui.tabs.full_auto module.") from e

# Common configurations or utilities
CONFIG = {
    "version": "1.0",
    "author": "erikg713",
}

def get_config(key, default=None):
    """
    Retrieve a configuration value.

    Args:
        key (str): The configuration key to retrieve.
        default (any): The default value if the key is not found.

    Returns:
        any: The configuration value or the default.
    """
    return CONFIG.get(key, default)
