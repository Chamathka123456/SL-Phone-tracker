#!/bin/bash

echo "Starting Sri Lankan Phone Tracker..."
echo ""

# Check if script exists
if [ ! -f "sl_tracker.py" ]; then
    echo "❌ Error: sl_tracker.py not found!"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    exit 1
fi

# Run the tracker
python3 sl_tracker.py
