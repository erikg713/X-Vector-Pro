import importlib
import warnings

# Attempt to import specific utilities, logging warnings on failure
try:
    from .logger import log, encrypt_log
except ImportError as e:
    warnings.warn(f"Failed to import 'logger' utilities: {e}", ImportWarning)

try:
    from .helper import some_utility_function
except ImportError as e:
    warnings.warn(f"Failed to import 'helper' utilities: {e}", ImportWarning)

try:
    from .network import create_connection
except ImportError as e:
    warnings.warn(f"Failed to import 'network' utilities: {e}", ImportWarning)

# Explicitly define the public API of this package
__all__ = [
    "log",
    "encrypt_log",
    "some_utility_function",
    "create_connection",
]

# Dynamic import functions
def get_logger():
    """
    Dynamically imports and returns the 'logger' module.
    Ensures the module is only loaded when needed.
    """
    try:
        return importlib.import_module(".logger", __package__)
    except ImportError as e:
        raise ImportError(f"Failed to load 'logger' module: {e}") from e

def get_helper():
    """
    Dynamically imports and returns the 'helper' module.
    Ensures the module is only loaded when needed.
    """
    try:
        return importlib.import_module(".helper", __package__)
    except ImportError as e:
        raise ImportError(f"Failed to load 'helper' module: {e}") from e

def get_network():
    """
    Dynamically imports and returns the 'network' module.
    Ensures the module is only loaded when needed.
    """
    try:
        return importlib.import_module(".network", __package__)
    except ImportError as e:
        raise ImportError(f"Failed to load 'network' module: {e}") from e
