#!/bin/bash

# Ensure the script is being executed in the directory it resides in
cd "$(dirname "$0")" || { echo "[!] Failed to navigate to script directory."; exit 1; }

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install it to run X-Vector Pro."
    exit 1
fi

# Check for required Python modules
REQUIRED_MODULES=("PyQt5" "requests" "numpy")  # Replace with actual dependencies
for module in "${REQUIRED_MODULES[@]}"; do
    if ! python3 -c "import ${module}" &> /dev/null; then
        echo "[!] Missing Python module: ${module}. Please install it using 'pip install ${module}'."
        exit 1
    fi
done

# Display usage information
if [[ "$1" == "--help" ]]; then
    echo "Usage: ./run.sh [options]"
    echo "Options:"
    echo "  --headless    Run in headless mode."
    echo "  --help        Show this help message."
    exit 0
fi

# Launching the application
echo "[*] Launching X-Vector Pro..."

if [[ "$1" == "--headless" ]]; then
    echo "[*] Running in headless mode..."
    if ! python3 main.py --headless; then
        echo "[!] Error: Failed to execute main.py in headless mode."
        exit 1
    fi
else
    echo "[*] Running GUI mode..."
    if ! python3 main_pyqt.py; then
        echo "[!] Error: Failed to execute main_pyqt.py in GUI mode."
        exit 1
    fi
fi

echo "[*] X-Vector Pro exited successfully."
