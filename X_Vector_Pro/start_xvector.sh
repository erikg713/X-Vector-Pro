#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Please install it." >&2
    exit 1
fi

# Start the app in background and log output
echo "[*] Launching X-Vector Pro..."
nohup python3 main.py > logs/xvector_output.log 2>&1 &
echo "[*] X-Vector Pro started in background. Log: logs/xvector_output.log"
