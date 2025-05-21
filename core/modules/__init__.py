"""
core.modules
============

This package contains core functional modules for X-Vector Pro Supreme,
the advanced cybersecurity toolkit.

Auto-discovers and imports available modules for streamlined development
and usage. Extend this package by adding new Python files in this directory.
"""

import importlib
import pkgutil

__all__ = []

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    # Exclude private modules
    if not module_name.startswith('_'):
        module = importlib.import_module(f"{__name__}.{module_name}")
        globals()[module_name] = module
        __all__.append(module_name)
