#!/bin/bash

echo "🚀 Starting Advanced Sri Lankan Phone Tracker..."
echo ""

cd "$(dirname "$0")"

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Running installer..."
    chmod +x install_advanced.sh
    ./install_advanced.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check for main script
if [ ! -f "sl_tracker_advanced.py" ]; then
    echo "Error: Main script not found!"
    exit 1
fi

# Run
python sl_tracker_advanced.py
