# core/__init__.py

import logging
import os
import json

# Setup and configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s"
)
logger = logging.getLogger("xvector.core")
logger.info("X-Vector Pro core package initialized.")

__version__ = "1.0.1"

def load_configuration(config_file=None):
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
            logger.warning(f"Failed to load config: {e}")
    else:
        logger.info("Using default configuration.")

    try:
        logging_level = default_config.get("logging_level", "INFO").upper()
        logging.getLogger().setLevel(logging_level)
        logger.setLevel(logging_level)
        logger.info(f"Logging level set to {logging_level}")
    except ValueError:
        logger.warning("Invalid logging level; defaulting to INFO.")
        logger.setLevel(logging.INFO)

    return default_config

def update_configuration(new_config):
    global configuration
    configuration.update(new_config)
    logger.info("Configuration updated.")
    return configuration

configuration = load_configuration()
