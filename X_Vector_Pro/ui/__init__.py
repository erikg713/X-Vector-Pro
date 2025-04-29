"""
UI package initializer for X-Vector Pro.
Exposes key UI modules, sets up shared resources, and initializes global components like the dashboard and notification manager.
"""

# Import core UI components for global access
from .dashboard import Dashboard
from .theme import DarkTheme  # Assuming you have a theming module
from .notifications import ToastManager  # For global toast access

# Global UI component instances
dashboard_instance = Dashboard()
toast_manager = ToastManager()

# Optional: Initialize and apply the theme globally (if your theme setup requires it)
def initialize_ui():
    """Initialize and configure global UI settings."""
    DarkTheme.apply_theme()  # If you want to apply dark mode globally on app startup

# Expose the components for external use
__all__ = ['Dashboard', 'dashboard_instance', 'DarkTheme', 'ToastManager', 'toast_manager', 'initialize_ui']
