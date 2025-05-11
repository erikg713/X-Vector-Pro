import os
import json
import time
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "xvector_log.txt")

os.makedirs(LOG_DIR, exist_ok=True)

def log_event(category, data, write_structured_file=False):
    """
    Log an event to both a rolling log file and optionally a timestamped structured JSON file.

    Args:
        category (str): e.g. "scan", "recon", "brute", "exploit"
        data (dict): Result or event data
        write_structured_file (bool): Whether to create a separate timestamped JSON file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Rolling append-only log file
    rolling_log = {
        "timestamp": time.time(),
        "category": category,
        "data": data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(rolling_log) + "\n")

    # Optional timestamped structured JSON file
    if write_structured_file:
        event_file = os.path.join(LOG_DIR, f"{category}_{timestamp}.json")
        structured_log = {
            "timestamp": timestamp,
            "category": category,
            "data": data
        }
        with open(event_file, "w") as f:
            json.dump(structured_log, f, indent=4)
        return event_file

    return LOG_FILE
