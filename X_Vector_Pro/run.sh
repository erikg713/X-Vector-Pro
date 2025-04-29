#!/bin/bash

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install it to run X-Vector Pro."
    exit 1
fi

echo "[*] Launching X-Vector Pro..."

if [[ "$1" == "--headless" ]]; then
    echo "[*] Running in headless mode..."
    python3 main.py --headless
else
    echo "[*] Running GUI mode..."
    python3 main_pyqt.py
fi
