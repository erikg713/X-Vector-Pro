import csv
from datetime import datetime

def log_session_result(session_id, status, details, file_path="data/sessions/results.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, session_id, status, details]
    try:
        file_exists = False
        try:
            with open(file_path, 'r', newline='') as f:
                file_exists = bool(f.readline())
        except FileNotFoundError:
            pass
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'session_id', 'status', 'details'])
            writer.writerow(row)
    except Exception as e:
        print(f"Failed to log session result: {e}")
