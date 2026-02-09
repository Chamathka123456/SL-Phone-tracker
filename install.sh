#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   Advanced Sri Lankan Phone Tracker Installer    ║
echo "║     With Real Geolocation & Google Maps          ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv 2>/dev/null || {
    sudo apt install -y python3-venv
    python3 -m venv venv
}

# Activate
source venv/bin/activate

# Install packages
echo "Installing required packages..."
pip install phonenumbers folium opencage requests

# Make scripts executable
chmod +x sl_tracker_advanced.py

echo ""
echo "══════════════════════════════════════════════════"
echo "✅ Installation Complete!"
echo ""
echo "To run the advanced tracker:"
echo "   source venv/bin/activate"
echo "   python sl_tracker_advanced.py"
echo ""
echo "📋 IMPORTANT: You need an OpenCage API key:"
echo "   1. Visit: https://opencagedata.com/api"
echo "   2. Sign up for FREE account"
echo "   3. Get API key (2500 requests/day free)"
echo "   4. Enter when prompted"
echo ""
echo "📍 Features:"
echo "   • Real addresses from Google Maps data"
echo "   • Exact coordinates (latitude/longitude)"
echo "   • Interactive maps"
echo "   • Google Maps & OpenStreetMap links"
echo "══════════════════════════════════════════════════"
echo ""
