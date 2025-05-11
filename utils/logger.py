# utils/logger.py

from core import logger

def log(message):
    logger.info(message)

def warn(message):
    logger.warning(message)

def error(message):
    logger.error(message)
