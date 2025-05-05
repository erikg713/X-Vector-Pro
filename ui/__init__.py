"""
UI package initializer for X-Vector Pro.
Exposes key UI modules, sets up shared resources, and initializes global components like the dashboard and notification manager.

Example:
    from ui import dashboard_instance, toast_manager, initialize_ui
    initialize_ui()
"""

import logging

logger = logging.getLogger(__name__)

# Import core UI components for global access
try:
    from .dashboard import Dashboard
    from .theme import DarkTheme  # Assuming you have a theming module
    from .notifications import ToastManager  # For global toast access
except ImportError as e:
    raise ImportError(f"Failed to import UI components: {e}")

# Lazy initialization for better performance
_dashboard_instance = None
_toast_manager = None

def get_dashboard_instance():
    """Get or initialize the dashboard instance."""
    global _dashboard_instance
    if _dashboard_instance is None:
        _dashboard_instance = Dashboard()
        logger.info("Dashboard instance initialized.")
    return _dashboard_instance

def get_toast_manager():
    """Get or initialize the toast manager."""
    global _toast_manager
    if _toast_manager is None:
        _toast_manager = ToastManager()
        logger.info("Toast manager initialized.")
    return _toast_manager

def initialize_ui(theme='DarkTheme'):
    """Initialize and configure global UI settings."""
    try:
        if theme == 'DarkTheme':
            DarkTheme.apply_theme()
            logger.info("Dark theme applied successfully.")
        else:
            logger.warning(f"Unknown theme: {theme}")
    except Exception as e:
        logger.error(f"Failed to apply theme: {e}")

# Expose the components for external use
__all__ = [
    'Dashboard', 'get_dashboard_instance', 'DarkTheme', 
    'ToastManager', 'get_toast_manager', 'initialize_ui'
]
