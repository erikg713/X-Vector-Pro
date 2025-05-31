#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X-Vector Pro Engine
==================

Core processing engine for security analysis and visualization.
Handles data processing, analysis workflows, and backend operations.

Note: For optimal performance, run with Python 3.9+ on systems with >8GB RAM.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

# Version tracking - update this when making significant changes
__version__ = '0.3.5'
__build__ = '20250531'  # YYYYMMDD format
__author__ = 'Erik G'

# Initialize engine logger
logger = logging.getLogger("xvector.engine")

# Define base paths
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = BASE_DIR / "cache"
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

# Ensure required directories exist
for directory in [CACHE_DIR, DATA_DIR, MODEL_DIR]:
    directory.mkdir(exist_ok=True)

# Runtime configuration
ENGINE_CONFIG = {
    'max_threads': 8,  # Adjust based on available cores
    'debug_mode': False,
    'accelerated': True,  # Use GPU acceleration when available
    'max_memory_gb': 4,  # Limit memory usage 
    'cache_ttl': 3600,   # Cache time-to-live in seconds
    'timeout': 30,       # Default operation timeout
}

# Track loaded modules for dependency management
_loaded_modules = {}
_initialized = False

# Import core components - do this after config to avoid circular imports
try:
    from .core import CoreProcessor, DataManager
    from .analysis import AnalysisEngine, ThreatScanner
    from .visualization import Visualizer
    # Perf enhancement from Frank - lazy load these heavy modules
    # from .ml import MachineLearning  # Disabled until we fix the numpy dependency hell
    _loaded_modules['core'] = True
    _loaded_modules['analysis'] = True
    _loaded_modules['visualization'] = True
    _loaded_modules['ml'] = False  # Currently disabled
except ImportError as e:
    logger.error(f"Failed to import engine components: {e}")
    # Don't crash, but track the failure
    _loaded_modules['error'] = str(e)

def initialize(config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Initialize the X-Vector engine with optional configuration override.
    
    Args:
        config: Optional configuration dictionary to override defaults
        
    Returns:
        bool: True if initialization succeeded
    """
    global _initialized, ENGINE_CONFIG
    
    if _initialized:
        logger.warning("Engine already initialized, skipping")
        return True
    
    start_time = time.time()
    logger.info(f"Initializing X-Vector Engine v{__version__}")
    
    # Update configuration if provided
    if config:
        ENGINE_CONFIG.update(config)
    
    # TODO: Add GPU detection and auto-config (issue #47)
    # For now just check if CUDA is available
    if ENGINE_CONFIG['accelerated']:
        try:
            # Moved this here from global scope - saves 200ms on startup
            import torch
            ENGINE_CONFIG['has_gpu'] = torch.cuda.is_available()
            if ENGINE_CONFIG['has_gpu']:
                logger.info(f"GPU acceleration enabled: {torch.cuda.get_device_name(0)}")
                # Somehow this makes torch faster with our models
                torch.backends.cudnn.benchmark = True
            else:
                logger.info("GPU acceleration not available, using CPU")
        except ImportError:
            ENGINE_CONFIG['has_gpu'] = False
            logger.warning("GPU acceleration requested but PyTorch not installed")
    
    try:
        # Initialize core components
        CoreProcessor.init(ENGINE_CONFIG)
        DataManager.init(ENGINE_CONFIG)
        
        # Validate model files
        _check_models()
        
        _initialized = True
        load_time = time.time() - start_time
        logger.info(f"Engine initialization complete ({load_time:.2f}s)")
        return True
        
    except Exception as e:
        logger.error(f"Engine initialization failed: {e}", exc_info=True)
        return False

def _check_models() -> None:
    """Check for required ML models and download if missing."""
    required_models = ['threat_classifier_v2.pt', 'network_analyzer.onnx']
    missing = []
    
    for model in required_models:
        if not (MODEL_DIR / model).exists():
            missing.append(model)
    
    # FIXME: Auto-download is broken on Windows after VS C++ update
    # See issue #92 - for now just warn the user
    if missing:
        logger.warning(f"Missing required models: {', '.join(missing)}")
        logger.warning(f"Download them from the releases page to {MODEL_DIR}")

def status() -> Dict[str, Any]:
    """
    Get current engine status and configuration.
    
    Returns:
        Dict with status information and configuration
    """
    return {
        'initialized': _initialized,
        'version': __version__,
        'build': __build__,
        'loaded_modules': _loaded_modules,
        'config': ENGINE_CONFIG,
        'paths': {
            'base': str(BASE_DIR),
            'cache': str(CACHE_DIR),
            'data': str(DATA_DIR),
            'models': str(MODEL_DIR),
        }
    }

def shutdown() -> None:
    """Gracefully shut down the engine and release resources."""
    global _initialized
    
    if not _initialized:
        logger.warning("Engine not initialized, nothing to shut down")
        return
    
    logger.info("Shutting down X-Vector Engine")
    
    # Close open resources - these can leak if not properly closed
    try:
        CoreProcessor.shutdown()
        DataManager.shutdown()
        
        # Explicitly clear cache to free memory
        if CACHE_DIR.exists():
            # Don't purge user data, just temp files
            for temp_file in CACHE_DIR.glob("temp_*.tmp"):
                try:
                    temp_file.unlink()
                except:
                    pass  # Best effort cleanup
                    
        _initialized = False
        logger.info("Engine shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Auto-initialize if not imported as a module
# This is a bit controversial but saves typing in simple use cases
if __name__ != "__main__" and os.environ.get('XVECTOR_AUTO_INIT', '1') == '1':
    initialize()