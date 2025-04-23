#!/bin/bash

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install it to run X-Vector Pro."
    exit 1
fi

if [[ "$1" == "--headless" ]]; then
    echo "[*] Launching X-Vector Pro in headless mode..."
    python3 main.py --headless
else
    echo "[*] Launching X-Vector Pro GUI..."
    python3 main_pyqt.py
fi
