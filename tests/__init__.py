#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X-Vector Pro GUI Tool - Test Suite
----------------------------------
Testing framework initialization and configuration.

Created: May 27, 2025
Author: Erik G.
"""

import os
import sys
import unittest
import warnings

# Add parent directory to path to make imports work in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Suppress ResourceWarnings about unclosed files during tests
warnings.filterwarnings("ignore", category=ResourceWarning)

# Define test constants
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
TEST_CONFIG = {
    'verbose': True,
    'fail_fast': False,
    'buffer_output': True,
    'use_mocks': True
}

# Ensure test data directory exists
if not os.path.exists(TEST_DATA_DIR):
    try:
        os.makedirs(TEST_DATA_DIR)
    except OSError as e:
        print(f"Warning: Couldn't create test data directory: {e}")

# Basic test runner configuration
def run_tests(pattern='test_*.py', verbosity=2):
    """Run all tests matching the pattern with specified verbosity."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern=pattern)
    test_runner = unittest.TextTestRunner(verbosity=verbosity)
    return test_runner.run(test_suite)

# Expose key test components
__all__ = ['run_tests', 'TEST_DATA_DIR', 'TEST_CONFIG']

# Initialize pytest integration if available
try:
    import pytest
    pytest_plugins = ["pytest_mock", "pytest_cov"]
except ImportError:
    pass  # pytest not required, using unittest framework

# Useful function for any test that needs temporary files
def get_temp_filename(prefix='test_', suffix='.tmp'):
    """Generate a temporary filename for test use."""
    import tempfile
    fd, filename = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)  # Close the file descriptor but keep the filename
    return filename
