# data/sessions/__init__.py
"""
This module initializes the sessions package, which handles user session management.
"""

from .session_manager import SessionManager

# Create a global session manager instance for package-wide use.
session_manager = SessionManager()

__all__ = ['session_manager', 'SessionManager']
