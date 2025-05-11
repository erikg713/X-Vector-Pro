"""
Core package for X-Vector Pro modules.

Module Metadata:
    Author  : Erik G.
    Version : 1.0.1
    Description: This package contains the central modules for the X-Vector Pro Supreme cybersecurity toolkit.
"""

import logging
import os
import json
from datetime import datetime 

# Configure logging for the package with a standardized format
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s"
)

logger = logging.getLogger("xvector.core")
logger.info("X-Vector Pro core package initialized.")

# Package version definition
__version__ = "1.0.1"

def load_configuration(config_file=None):
    """
    Load application configuration from an external JSON file or use default settings.

    Args:
        config_file (str, optional): Path to a JSON configuration file.

    Returns:
        dict: A dictionary containing configuration settings.
    """
    # Default configuration values
    default_config = {
        "setting_a": True,
        "setting_b": 10,
        "setting_c": "default",
        "logging_level": "INFO",
        "stealth_mode": False
    }

    # Try to load configuration from a file if provided
    if config_file and os.path.isfile(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            default_config.update(file_config)
            logger.info(f"Configuration loaded from {config_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {config_file}: {e}")
        except Exception as e:
            logger.warning(f"Failed to load config from {config_file}: {e}")
            logger.info("Reverting to default configuration.")
    else:
        logger.info("No config file provided or file not found, using default configuration.")

    # Adjust the logging level based on configuration setting
    try:
        logging_level = default_config.get("logging_level", "INFO").upper()
        logging.basicConfig(level=logging_level)
        logger.setLevel(logging_level)
        logger.info(f"Logging level set to {logging_level}")
    except ValueError:
        logger.warning(f"Invalid logging level in config, defaulting to INFO.")
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(logging.INFO)

    return default_config

def update_configuration(new_config):
    """
    Update the global configuration with new settings.

    Args:
        new_config (dict): New configuration values to apply.

    Returns:
        dict: Updated configuration dictionary.
    """
    global configuration
    configuration.update(new_config)
    logger.info("Configuration updated.")
    return configuration

# Initialize and expose the package configuration globally
configuration = load_configuration()
