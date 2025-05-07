"""
Core package for X-Vector Pro modules.

Module Metadata:
    Author  : Erik G.
    Version : 1.0.0
    Description: This package contains the central modules for the X-Vector Pro Supreme cybersecurity toolkit.
"""

import logging
import os
import json

# Configure logging for the package with a standardized format
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s"
)

logger = logging.getLogger("xvector.core")
logger.info("X-Vector Pro core package initialized.")

# Package version definition
__version__ = "1.0.0"

def load_configuration(config_file=None):
    """
    Load application configuration from an external JSON file or use default settings.

    Args:
        config_file (str, optional): Path to a JSON configuration file.

    Returns:
        dict: A dictionary containing configuration settings.
    """
    default_config = {
        "setting_a": True,
        "setting_b": 10,
        "setting_c": "default",
        "logging_level": "INFO",
        "stealth_mode": False
    }

    if config_file and os.path.isfile(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            default_config.update(file_config)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.warning(f"Failed to load config from {config_file}: {e}")
            logger.info("Reverting to default configuration.")
    else:
        logger.info("Using default configuration settings.")
    
    return default_config

# Initialize and expose the package configuration globally
configuration = load_configuration()
