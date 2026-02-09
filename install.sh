#!/bin/bash

# Sri Lankan Phone Tracker - Installation Script
# For Kali Linux with virtual environment support

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   🇱🇰 Sri Lankan Phone Tracker - Installer       ║
echo "║        Advanced Edition with Maps               ║
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

cd "$(dirname "$0")"

# Check Python
echo -e "${BLUE}[1/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 not found! Installing...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
    echo -e "${GREEN}✅ Python3 installed${NC}"
else
    echo -e "${GREEN}✅ Python3 is installed${NC}"
fi

# Create virtual environment
echo -e "\n${BLUE}[2/5]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Installing python3-venv...${NC}"
        sudo apt install -y python3-venv
        python3 -m venv venv
    fi
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate and install packages
echo -e "\n${BLUE}[3/5]${NC} Installing Python packages..."
source venv/bin/activate

echo "Installing phonenumbers..."
pip install phonenumbers

echo "Installing opencage..."
pip install opencage

echo "Installing folium..."
pip install folium

echo -e "${GREEN}✅ All packages installed${NC}"

# Make scripts executable
echo -e "\n${BLUE}[4/5]${NC} Setting up scripts..."
chmod +x sl_tracker_advanced.py 2>/dev/null
chmod +x run.sh 2>/dev/null
chmod +x quick_test.py 2>/dev/null
echo -e "${GREEN}✅ Scripts made executable${NC}"

# Create API key file template
echo -e "\n${BLUE}[5/5]${NC} Setting up API key..."
if [ ! -f "api_key.txt" ]; then
    echo "YOUR_API_KEY_HERE" > api_key.txt
    echo -e "${YELLOW}⚠️  API key file created (api_key.txt)${NC}"
    echo -e "${YELLOW}   Get FREE key from: https://opencagedata.com/api${NC}"
fi

echo ""
echo "══════════════════════════════════════════════════"
echo -e "${GREEN}✅ INSTALLATION COMPLETE!${NC}"
echo "══════════════════════════════════════════════════"
echo ""
echo "To run the tracker:"
echo -e "  ${BLUE}source venv/bin/activate${NC}"
echo -e "  ${BLUE}python sl_tracker_advanced.py${NC}"
echo ""
echo "Or use the run script:"
echo -e "  ${BLUE}./run.sh${NC}"
echo ""
echo -e "${YELLOW}📋 IMPORTANT:${NC}"
echo "1. Get FREE API key from: https://opencagedata.com"
echo "2. Edit api_key.txt and add your key"
echo "3. For exact locations and maps, API key is required"
echo ""
echo -e "${GREEN}📞 Test with: 0770851207 or +94701234567${NC}"
echo "══════════════════════════════════════════════════"
echo ""
