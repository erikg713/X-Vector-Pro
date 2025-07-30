import os
import logging
from logging.handlers import RotatingFileHandler
import logging
import os

def create_logger(name="XVectorPro", log_level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent duplicate handlers if this function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def create_logger(log_dir="logs", log_file="xvector.log", max_bytes=1_000_000, backup_count=5):
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, log_file)

    logger = logging.getLogger("XVectorLogger")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
