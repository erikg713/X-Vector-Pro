import os
import logging
from logging.handlers import RotatingFileHandler

def create_logger(
    name="XVectorPro",
    log_level=logging.INFO,
    log_dir="logs",
    log_file="xvector.log",
    max_bytes=1_000_000,
    backup_count=5,
    console_output=True
):
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, log_file)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    if console_output:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    fh = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
