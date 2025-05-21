import os
from datetime import datetime

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), 'results.txt'
)

HEADER = (
    "# X-Vector Pro Supreme - Session Results Log\n"
    "# Format: [timestamp] | [session_id] | [user] | [status] | [scanned_targets] | [vulnerabilities_found] | [notes]\n"
    "# All timestamps are UTC, ISO 8601.\n"
    "# Status: COMPLETED, ERROR, IN_PROGRESS\n"
)

def ensure_header():
    # Only add header if file is missing or empty
    if not os.path.exists(RESULTS_FILE) or os.stat(RESULTS_FILE).st_size == 0:
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            f.write(HEADER)

def log_session(session_id, user, status, scanned_targets, vulnerabilities_found, notes=""):
    ensure_header()
    timestamp = datetime.utcnow().isoformat() + "Z"
    entry = f"{timestamp} | {session_id} | {user} | {status} | {scanned_targets} | {vulnerabilities_found} | {notes}\n"
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

# Example usage:
if __name__ == "__main__":
    log_session(
        session_id="d4f9b2",
        user="erikg713",
        status="COMPLETED",
        scanned_targets=156,
        vulnerabilities_found=3,
        notes="Routine scan, no critical issues."
    )
