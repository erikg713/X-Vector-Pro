#!/bin/bash

# Define the root directory for the X-Vector Pro toolkit
TOOLKIT_DIR="/opt/xvectorpro"

# Check if the toolkit directory exists
if [ ! -d "$TOOLKIT_DIR" ]; then
    echo "Error: Toolkit directory $TOOLKIT_DIR does not exist!" >&2
    exit 1
fi

# Navigate to the toolkit directory
if cd "$TOOLKIT_DIR"; then
    echo "Successfully navigated to $TOOLKIT_DIR"
else
    echo "Error: Failed to navigate to $TOOLKIT_DIR" >&2
    exit 1
fi

# Ensure all dependencies are loaded
echo "Initializing toolkit dependencies..."
if [ -f "initialize.sh" ]; then
    bash initialize.sh
    if [ $? -ne 0 ]; then
        echo "Error: Failed to initialize dependencies!" >&2
        exit 1
    fi
else
    echo "Warning: initialize.sh not found. Skipping initialization."
fi

# Start the main toolkit script
MAIN_SCRIPT="start_xvector.sh"
if [ -x "$MAIN_SCRIPT" ]; then
    echo "Starting the X-Vector Pro toolkit..."
    bash "$MAIN_SCRIPT"
    if [ $? -eq 0 ]; then
        echo "X-Vector Pro toolkit started successfully."
    else
        echo "Error: $MAIN_SCRIPT encountered an error!" >&2
        exit 1
    fi
else
    echo "Error: $MAIN_SCRIPT not found or not executable." >&2
    exit 1
fi

# Optional: Launch additional components (e.g., GUI, monitoring tools)
echo "Launching additional toolkit components..."
if [ -f "gui_launcher.sh" ]; then
    bash gui_launcher.sh
    if [ $? -eq 0 ]; then
        echo "GUI launched successfully."
    else
        echo "Error: GUI launcher encountered an error!" >&2
    fi
else
    echo "Warning: GUI launcher script not found. Skipping."
fi

# Final status message
echo "X-Vector Pro toolkit is fully operational."
exit 0
