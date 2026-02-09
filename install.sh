#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   Sri Lankan Phone Tracker - Installation    ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
    echo "✅ Python3 installed"
else
    echo "✅ Python3 is installed"
fi

# Install pip if not present
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt install -y python3-pip
fi

# Install required package
echo "Installing required package: phonenumbers..."
pip3 install phonenumbers --user

# Make main script executable
chmod +x sl_tracker.py

echo ""
echo "══════════════════════════════════════════════"
echo "✅ Installation Complete!"
echo ""
echo "To run the tracker:"
echo "   ./sl_tracker.py"
echo ""
echo "Or using Python directly:"
echo "   python3 sl_tracker.py"
echo ""
echo "Enter Sri Lankan phone numbers when prompted."
echo "Examples: +94701234567 or 0701234567"
echo "══════════════════════════════════════════════"
echo ""
