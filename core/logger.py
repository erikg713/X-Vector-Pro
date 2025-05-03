import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(category, data):
    """
    Log a structured event to a JSON log file.

    Args:
        category (str): e.g. "scan", "recon", "brute", "exploit"
        data (dict): Your scan result, brute result, etc.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{category}_{timestamp}.json")

    log_data = {
        "timestamp": timestamp,
        "category": category,
        "data": data
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    return log_file
