#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install it to run X-Vector Pro."
    exit 1
fi

echo "[*] Launching X-Vector Pro GUI..."
python3 main_pyqt.py
