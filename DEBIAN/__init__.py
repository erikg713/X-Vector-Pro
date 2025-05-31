#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBIAN package initialization for X-Vector Pro GUI Tool
Handles package-specific setup and configurations

Created: May 14, 2025
Updated: May 31, 2025
Author: Erik G.
"""

import os
import sys
import logging
from pathlib import Path

# Set up package logging
logger = logging.getLogger("xvector.debian")

# Package constants
__version__ = '0.3.5'  # Keep in sync with debian/changelog
__codename__ = 'sierra'
__maintainer__ = 'erikg713 <erik@x-vector-security.io>'

# Find base directory - bit hacky but works better than hardcoding
_BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Package directories - used by maintainer scripts
BIN_DIR = _BASE_DIR / 'bin'
SHARE_DIR = Path('/usr/share/x-vector-pro')
CONFIG_DIR = Path('/etc/x-vector-pro')

# Check if we're running during package installation
DPKG_INSTALL = os.environ.get('DPKG_MAINTSCRIPT_PACKAGE') == 'x-vector-pro'

# Required dependencies - helps with runtime checks
SYSTEM_DEPENDENCIES = [
    'libc6 (>= 2.33)',
    'libgtk-3-0 (>= 3.24.0)',
    'python3 (>= 3.9)',
    'python3-gi',
    'gir1.2-gtk-3.0'
]

# Sometimes these files are missing in weird edge cases
CRITICAL_FILES = [
    '/usr/bin/x-vector-pro',
    '/usr/share/x-vector-pro/app.py',
    '/usr/share/x-vector-pro/resources/icon.png',
    '/etc/x-vector-pro/config.ini'
]

def check_installation():
    """Verify that the Debian package is correctly installed"""
    errors = []
    
    # Frank had this break on him once due to permissions
    try:
        for file_path in CRITICAL_FILES:
            if not os.path.exists(file_path):
                errors.append(f"Missing file: {file_path}")
    except PermissionError:
        # This sometimes happens if run as non-root user
        logger.warning("Permission error checking installation files")
        return False
    
    if errors:
        logger.error("Installation verification failed:")
        for err in errors:
            logger.error(f"  - {err}")
        return False
        
    return True

def get_system_info():
    """Return information about the Debian system"""
    # Parse /etc/os-release to get distro info
    info = {}
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    # Remove quotes if they exist
                    info[key] = value.strip('"\'')
    except (IOError, FileNotFoundError):
        # Fallback if can't read os-release
        info['ID'] = 'unknown'
        info['VERSION_ID'] = '0'
    
    # Add some extra info that's useful for diagnostics
    try:
        import platform
        import subprocess
        
        kernel = platform.release()
        
        # Check desktop environment
        desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
        
        # Try to get graphics info - useful for display issues
        try:
            gpu_info = subprocess.check_output(
                "lspci | grep -i 'vga\\|3d\\|2d'", 
                shell=True, text=True
            ).strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            gpu_info = "Unknown"
            
        info.update({
            'KERNEL': kernel,
            'DESKTOP_ENV': desktop_env,
            'GPU': gpu_info[:100] if len(gpu_info) > 100 else gpu_info
        })
    except Exception as e:  # Something weird happened
        logger.warning(f"Couldn't get complete system info: {e}")
    
    return info

# Initialize configuration on import if in package context
if DPKG_INSTALL:
    try:
        logger.info(f"Initializing X-Vector Pro {__version__} in Debian package context")
        
        # Ensure config dir exists and has appropriate permissions
        if not CONFIG_DIR.exists():
            logger.warning(f"Config directory missing, creating: {CONFIG_DIR}")
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            # This could be tighter, but works for now
            os.chmod(CONFIG_DIR, 0o755)
        
    except Exception as e:
        logger.error(f"Failed during Debian package initialization: {e}")
        # Don't raise - we're during package init and should continue

# Prevent execution of this file directly
if __name__ == "__main__":
    print(f"X-Vector Pro {__version__} ({__codename__})")
    print("This module is not meant to be executed directly.")
    print("For diagnostics, run: x-vector-pro --check")
    sys.exit(1)