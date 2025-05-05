"""
Core package for X-Vector Pro modules.

Module Metadata:
    Author  : Erik G.
    Version : 1.0.0
    Description: This package contains the central modules for the X-Vector Pro Supreme cybersecurity toolkit.
"""

import logging
import os

# Configure logging for the package with a standardized format
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s")
logger = logging.getLogger(__name__)
logger.info("X-Vector Pro core package initialized.")

# Package version definition
__version__ = "1.0.0"

def load_configuration(config_file=None):
    """
    Load application configuration from an external file or fall back to default settings.

    Args:
        config_file (str, optional): Path to a configuration file. Defaults to None.

    Returns:
        dict: A dictionary containing configuration settings.
    """
    default_config = {
        "setting_a": True,
        "setting_b": 10,
        "setting_c": "default"
    }
    
    if config_file and os.path.isfile(config_file):
        logger.info(f"Loading configuration from {config_file}")
        # Simulate loading configuration from file
        # In a real scenario, you'd parse the configuration file here (e.g., using json or yaml)
        default_config['setting_c'] = "loaded from file"
    else:
        logger.info("Using default configuration settings.")
    
    return default_config

# Initialize and expose the package configuration globally
configuration = load_configuration()
