#!/bin/bash

# Sri Lankan Phone Tracker - Runner Script

echo ""
echo "🚀 Starting Sri Lankan Phone Tracker..."
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Running installer first..."
    
    if [ -f "install.sh" ]; then
        chmod +x install.sh
        ./install.sh
    else
        echo "⚠️ Install script not found!"
        echo "Please run manually:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install phonenumbers opencage folium"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check for main script
if [ ! -f "sl_tracker_advanced.py" ]; then
    echo "❌ Main tracker script not found!"
    echo "Available files:"
    ls -la *.py
    exit 1
fi

# Run the tracker
echo ""
echo "🇱🇰 Launching tracker..."
echo "══════════════════════════════════════════════════"
echo ""

python sl_tracker_advanced.py
