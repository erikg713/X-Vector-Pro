#!/bin/bash

# Move to the script's directory
cd "$(dirname "$0")" || { echo "[!] Failed to change directory." >&2; exit 1; }

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is missing. Please install it." >&2
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "[*] Using Python: $PYTHON_VERSION"

# Validate presence of main.py
if [[ ! -f "main.py" ]]; then
    echo "[!] Error: 'main.py' not found in current directory." >&2
    exit 1
fi

# Set up logs directory with secure permissions
LOG_DIR="logs"
mkdir -p "$LOG_DIR" && chmod 700 "$LOG_DIR"

# Rotate old logs with timestamp
LOG_FILE="$LOG_DIR/xvector_output.log"
if [[ -f "$LOG_FILE" ]]; then
    mv "$LOG_FILE" "$LOG_DIR/xvector_output_$(date +%F_%T).log"
fi

# Check for existing process
PID_FILE="$LOG_DIR/xvector_pid.txt"
if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(<"$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null; then
        echo "[!] X-Vector Pro is already running (PID: $OLD_PID)."
        exit 0
    fi
fi

# Launch the application in the background
echo "[*] Starting X-Vector Pro..."
nohup python3 main.py > "$LOG_FILE" 2>&1 &

# Validate startup success
if [[ $? -ne 0 ]]; then
    echo "[!] Failed to start X-Vector Pro." >&2
    exit 1
fi

# Store process ID securely
echo $! > "$PID_FILE"
chmod 600 "$PID_FILE"

echo "[*] X-Vector Pro is running in the background."
echo "[*] Log file: $LOG_FILE"
echo "[*] Process ID saved to: $PID_FILE"
