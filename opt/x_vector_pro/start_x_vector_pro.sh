#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")" || { echo "[!] Failed to change directory." >&2; exit 1; }

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Please install it." >&2
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "[*] Detected Python version: $PYTHON_VERSION"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "[!] main.py not found in the current directory. Please ensure it exists."
    exit 1
fi

# Check if logs directory exists; create if not
if [ ! -d "logs" ]; then
    mkdir logs || { echo "[!] Failed to create logs directory." >&2; exit 1; }
    chmod 700 logs
fi

# Rotate old log
if [ -f "logs/xvector_output.log" ]; then
    mv logs/xvector_output.log logs/xvector_output_$(date +%F_%T).log
fi

# Check if another process is already running
if [ -f "logs/xvector_pid.txt" ]; then
    OLD_PID=$(cat logs/xvector_pid.txt)
    if ps -p $OLD_PID > /dev/null; then
        echo "[!] X-Vector Pro is already running with PID $OLD_PID."
        exit 0
    fi
fi

# Start the app in background and log output
echo "[*] Launching X-Vector Pro..."
nohup python3 main.py > logs/xvector_output.log 2>&1 &
if [ $? -ne 0 ]; then
    echo "[!] Failed to launch X-Vector Pro." >&2
    exit 1
fi

# Save PID and set permissions
echo $! > logs/xvector_pid.txt
chmod 600 logs/xvector_pid.txt

echo "[*] X-Vector Pro started in background. Log: logs/xvector_output.log"
echo "[*] Process ID saved to logs/xvector_pid.txt"
