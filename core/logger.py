import os
import json
import time
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "xvector_log.txt")
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1 MB
BACKUP_COUNT = 3

os.makedirs(LOG_DIR, exist_ok=True)

# Setup rotating log handler
logger = logging.getLogger("XVectorLogger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_event(category, data, level="INFO", write_structured_file=False):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    message = json.dumps({"category": category, "data": data})

    try:
        if level.upper() == "INFO":
            logger.info(message)
        elif level.upper() == "ERROR":
            logger.error(message)
        elif level.upper() == "DEBUG":
            logger.debug(message)
        elif level.upper() == "WARNING":
            logger.warning(message)
        else:
            logger.info(message)
    except Exception as e:
        print(f"[!] Logging failed: {e}")

    if write_structured_file:
        try:
            structured_log = {
                "timestamp": timestamp,
                "level": level,
                "category": category,
                "data": data
            }
            event_file = os.path.join(LOG_DIR, f"{category}_{timestamp}.json")
            with open(event_file, "w") as f:
                json.dump(structured_log, f, indent=4)
            return event_file
        except Exception as e:
            print(f"[!] Failed to write structured log: {e}")

    return LOG_FILE


import os
import json
import time
from datetime import datetime
from utils.setup_logger import create_logger

logger = create_logger()

def log_event(category, data, level="info", write_structured_file=False, log_dir="logs"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    payload = {
        "timestamp": time.time(),
        "category": category,
        "data": data
    }

    try:
        msg = json.dumps(payload)
        getattr(logger, level.lower(), logger.info)(msg)

        if write_structured_file:
            file_name = f"{category}_{timestamp}.json"
            full_path = os.path.join(log_dir, file_name)
            with open(full_path, "w") as f:
                json.dump(payload, f, indent=4)
            return full_path

    except Exception as e:
        logger.error(f"Logging failed: {e}")

    return os.path.join(log_dir, "xvector.log")
