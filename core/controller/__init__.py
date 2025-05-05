"""
Initialization file for the core.controller module.

This module is responsible for managing and controlling core operations in the X-Vector Pro Supreme toolkit.
It provides utility functions, task scheduling, and centralized access to package components.
"""

# Import necessary components from the package
from .controller_utils import ControllerUtils
from .task_scheduler import TaskScheduler
from .logging_manager import LoggingManager  # Example: Add a logging component
from .config_loader import ConfigLoader  # Example: Add a configuration loading component

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
    "max_tasks": 10,  # Example: Maximum number of tasks to handle concurrently
}

# Logging Manager Initialization
logging_manager = LoggingManager(level=DEFAULT_CONFIG["logging_level"])

# Configuration Loader
config = ConfigLoader()
current_config = config.load_config()  # Load dynamic configurations (if any)

# Initialize Task Scheduler
task_scheduler = TaskScheduler(max_tasks=DEFAULT_CONFIG["max_tasks"])

def initialize_controller():
    """
    Perform necessary initialization for the controller module.
    This includes setting up logging, loading configurations, and initializing components.
    """
    logging_manager.log("Initializing core.controller module...", level="INFO")
    
    if DEFAULT_CONFIG["debug"]:
        logging_manager.log("Debug mode enabled for core.controller", level="DEBUG")
    
    # Example: Perform any additional startup checks or setup
    if not task_scheduler.is_ready():
        logging_manager.log("Task Scheduler is not ready. Initializing...", level="WARNING")
        task_scheduler.initialize()

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
