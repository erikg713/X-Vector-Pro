"""
Initialization file for the core.controller module.

This module is responsible for managing and controlling core operations in the X-Vector Pro Supreme toolkit.
It provides utility functions, task scheduling, and centralized access to package components.
"""

# Import necessary components from the package
from .controller_utils import ControllerUtils
from .task_scheduler import TaskScheduler
from .logging_manager import LoggingManager
from .config_loader import ConfigLoader

# Define the public API of the module
__all__ = [
    "ControllerUtils",
    "TaskScheduler",
    "LoggingManager",
    "ConfigLoader",
]

# Global Configuration
DEFAULT_CONFIG = {
    "debug": False,
    "logging_level": "INFO",
    "max_tasks": 10,
}

# Logging Manager Initialization
logging_manager = LoggingManager(level=DEFAULT_CONFIG["logging_level"])

# Configuration Loader
config_loader = ConfigLoader()
try:
    current_config = config_loader.load_config()
    # Merge default and loaded configurations
    current_config = {**DEFAULT_CONFIG, **current_config}
except Exception as e:
    logging_manager.log(f"Error loading configuration: {e}", level="ERROR")
    current_config = DEFAULT_CONFIG

# Initialize Task Scheduler
task_scheduler = TaskScheduler(max_tasks=current_config["max_tasks"])

def initialize_controller():
    """
    Perform necessary initialization for the controller module.
    This includes setting up logging, loading configurations, and initializing components.
    """
    logging_manager.log("Initializing core.controller module...", level="INFO")
    
    if current_config["debug"]:
        logging_manager.log("Debug mode enabled for core.controller", level="DEBUG")
    
    # Perform additional startup checks or setup
    if not task_scheduler.is_ready():
        logging_manager.log("Task Scheduler is not ready. Initializing...", level="WARNING")
        try:
            task_scheduler.initialize()
        except Exception as e:
            logging_manager.log(f"Error initializing Task Scheduler: {e}", level="ERROR")

# Call the initialization function
initialize_controller()

# Optional: Utility Functions (Extend Functionality)
def show_status():
    """
    Display the current status of the controller module.
    """
    status = {
        "Logging Level": logging_manager.current_level,
        "Loaded Configurations": current_config,
        "Task Scheduler Status": "Ready" if task_scheduler.is_ready() else "Not Ready",
    }
    for key, value in status.items():
        print(f"{key}: {value}")

# Example: Add a command-line entry point for debugging purposes
if __name__ == "__main__":
    print("Running core.controller as a standalone module for debugging...")
    show_status()
