import os
import json
import time
from datetime import datetime
from utils.setup_logger import create_logger
import logging

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'xvectorpro.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('XVectorPro')

# Override logger with custom logger if needed
custom_logger = create_logger()
if custom_logger:
    logger = custom_logger

def log_event(category, data, level="info", write_structured_file=False, log_dir=LOG_DIR):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    payload = {
        "timestamp": time.time(),
        "category": category,
        "data": data
    }

    try:
        msg = json.dumps(payload)
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(msg)

        if write_structured_file:
            os.makedirs(log_dir, exist_ok=True)
            file_name = f"{category}_{timestamp}.json"
            full_path = os.path.join(log_dir, file_name)
            with open(full_path, "w") as f:
                json.dump(payload, f, indent=4)
            return full_path

    except Exception as e:
        logger.error(f"Logging failed: {e}")

    return os.path.join(log_dir, "xvector.log")
