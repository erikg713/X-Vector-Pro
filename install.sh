#!/bin/bash
set -euo pipefail

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
NC="\033[0m"

echo -e "${GREEN}[*] Installing X-Vector Pro dependencies...${NC}"
sleep 1

# Update system packages
echo -e "${YELLOW}[*] Updating package list...${NC}"
sudo apt update || { echo -e "${RED}[!] Failed to update packages.${NC}"; exit 1; }

# Install essential system packages
echo -e "${YELLOW}[*] Installing required system packages...${NC}"
sudo apt install -y python3-tk build-essential firefox-esr wget curl unzip git python3-pip || {
    echo -e "${RED}[!] System package installation failed.${NC}"; exit 1;
}

# Install GeckoDriver for Selenium
echo -e "${YELLOW}[*] Installing GeckoDriver for Selenium...${NC}"
GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
wget -q "https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VERSION/geckodriver-v$GECKO_VERSION-linux64.tar.gz" -O geckodriver.tar.gz
tar -xzf geckodriver.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
rm geckodriver.tar.gz

# Upgrade pip and install Python modules
echo -e "${YELLOW}[*] Upgrading pip and installing Python modules...${NC}"
python3 -m pip install --upgrade pip

python3 -m pip install requests customtkinter tldextract \
    beautifulsoup4 lxml scapy aiohttp rich \
    python-nmap email-validator psutil netifaces \
    selenium paramiko || { echo -e "${RED}[!] Python module installation failed.${NC}"; exit 1; }

# Clone X-Vector Pro repository
echo -e "${YELLOW}[*] Cloning X-Vector Pro repository...${NC}"
git clone https://github.com/erikg713/X-Vector-Pro.git || {
    echo -e "${RED}[!] Failed to clone the repository.${NC}"
    exit 1
}

cd X-Vector-Pro
chmod +x run.sh

echo -e "${GREEN}[*] All dependencies installed successfully!${NC}"
echo -e "${GREEN}[*] X-Vector Pro is ready to run using: ./run.sh${NC}"
