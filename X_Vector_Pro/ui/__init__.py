# X_Vector_Pro/ui/__init__.py

"""
UI package initializer for X_Vector_Pro.
Exposes key UI modules and sets up shared resources.
"""

# Import core UI components here if needed for global access
from .dashboard import Dashboard
from .theme import DarkTheme  # If you have a theming module
from .notifications import ToastManager  # For global toast access

# Initialize global UI managers or settings if applicable
dashboard_instance = Dashboard()
toast_manager = ToastManager()

__all__ = ['Dashboard', 'dashboard_instance', 'DarkTheme', 'ToastManager', 'toast_manager']
