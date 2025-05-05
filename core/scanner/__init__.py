"""
Scanner module initializer for X_Vector_Pro.

This module exposes key scanner components such as PortScanner, 
VulnerabilityScanner, and DirectoryScanner for use in the core engine.

Example Usage:
    from core.scanner import PortScanner

    scanner = PortScanner()
    scanner.scan(target="192.168.1.1")
"""

try:
    from .port_scanner import PortScanner
except ImportError as e:
    raise ImportError("Failed to import PortScanner. Ensure all dependencies are installed.") from e

try:
    from .vuln_scanner import VulnerabilityScanner
except ImportError as e:
    raise ImportError("Failed to import VulnerabilityScanner. Ensure all dependencies are installed.") from e

try:
    from .dir_scanner import DirectoryScanner
except ImportError as e:
    raise ImportError("Failed to import DirectoryScanner. Ensure all dependencies are installed.") from e

__all__ = [
    'PortScanner', 
    'VulnerabilityScanner', 
    'DirectoryScanner'
]

if __name__ == "__main__":
    print("Available scanners:", __all__)
