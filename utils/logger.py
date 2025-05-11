from core import logger
from datetime import datetime 
def log(message):
    logger.info(message)

def warn(message):
    logger.warning(message)

def error(message):
    logger.error(message)

def log_to_central(msg, logs_output):
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs_output.insert("end", f"[{timestamp}] {msg}\n")
    logs_output.see("end")  # auto-scroll
