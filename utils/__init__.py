"""
This module simplifies imports for utility functions used across the project.
"""

__all__ = [
    "log",
    "encrypt_log",
    "some_utility_function",
    "create_connection",
]

try:
    from .logger import log, encrypt_log
except ImportError as e:
    print(f"Warning: Failed to import logger utilities: {e}")

try:
    from .helper import some_utility_function
except ImportError as e:
    print(f"Warning: Failed to import helper utilities: {e}")

try:
    from .network import create_connection
except ImportError as e:
    print(f"Warning: Failed to import network utilities: {e}")
