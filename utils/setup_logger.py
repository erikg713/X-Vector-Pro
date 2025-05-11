import os
import logging
from logging.handlers import RotatingFileHandler

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
