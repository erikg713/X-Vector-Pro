# core/__init__.py
# Core package initialization
from .brute_force_wallet import BruteEngine
from .config import Config
from .logger import logger
import logging
import os
import json
from typing import Optional, Dict, Any

# Setup and configure logging
def configure_logging(level: str = "INFO") -> None:
    """Configure logging for the core package."""
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s"
    )
    logger.setLevel(level)

logger = logging.getLogger("xvector.core")
configure_logging()
logger.info("X-Vector Pro core package initialized.")

# Package version
__version__ = "1.0.1"

# Default configuration
DEFAULT_CONFIG = {
    "setting_a": True,
    "setting_b": 10,
    "setting_c": "default",
    "logging_level": "INFO",
    "stealth_mode": False
}

def load_configuration(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a file, falling back to default settings.

    Args:
        config_file (Optional[str]): Path to the configuration file.

    Returns:
        Dict[str, Any]: The loaded configuration.
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_file:
        if os.path.isfile(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                config.update(file_config)
                logger.info(f"Configuration loaded from {config_file}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in config file: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading config file: {e}")
        else:
            logger.warning(f"Config file {config_file} does not exist. Using default configuration.")

    # Set logging level
    try:
        logging_level = config.get("logging_level", "INFO").upper()
        configure_logging(logging_level)
        logger.info(f"Logging level set to {logging_level}")
    except ValueError:
        logger.warning("Invalid logging level; defaulting to INFO.")
        configure_logging("INFO")

    return config

def update_configuration(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the current configuration.

    Args:
        new_config (Dict[str, Any]): A dictionary of new configuration settings.

    Returns:
        Dict[str, Any]: The updated configuration.
    """
    global configuration
    if not isinstance(new_config, dict):
        logger.error("Invalid configuration format. Must be a dictionary.")
        return configuration

    configuration.update(new_config)
    logger.info("Configuration updated.")
    return configuration

# Initialize configuration
configuration = load_configuration()
