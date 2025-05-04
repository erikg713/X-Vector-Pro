#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Please install it." >&2
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "[!] main.py not found in the current directory. Please ensure it exists."
    exit 1
fi

# Check if logs directory exists; create if not
if [ ! -d "logs" ]; then
    mkdir logs
fi

# Start the app in background and log output
echo "[*] Launching X-Vector Pro..."
nohup python3 main.py > logs/xvector_output.log 2>&1 &
echo $! > logs/xvector_pid.txt
echo "[*] X-Vector Pro started in background. Log: logs/xvector_output.log"
echo "[*] Process ID saved to logs/xvector_pid.txt"
