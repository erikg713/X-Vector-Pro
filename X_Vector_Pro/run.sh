#!/bin/bash

# Navigate to script's directory
cd "$(dirname "$0")"

# Launch the app with Python 3 and handle errors
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it to continue."
    exit 1
fi

python3 main.py
