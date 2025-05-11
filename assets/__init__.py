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
