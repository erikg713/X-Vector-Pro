#!/bin/bash

echo "[*] Installing X-Vector Pro dependencies..."
sleep 1

# Update package list
echo "[*] Updating package list..."
sudo apt update || { echo "[!] Failed to update packages."; exit 1; }

# Install system packages
echo "[*] Installing system packages (python3-tk, build-essential, browser drivers)..."
sudo apt install python3-tk build-essential firefox-esr -y || { echo "[!] Failed to install system packages."; exit 1; }

# Optional: Install GeckoDriver for Firefox automation with Selenium
echo "[*] Installing GeckoDriver for Selenium..."
GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
wget -q "https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VERSION/geckodriver-v$GECKO_VERSION-linux64.tar.gz" -O geckodriver.tar.gz
tar -xzf geckodriver.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver.tar.gz

# Upgrade pip and install Python packages
echo "[*] Installing Python modules..."
pip install --upgrade pip

pip install requests customtkinter tldextract \
    beautifulsoup4 lxml scapy aiohttp rich \
    python-nmap email-validator psutil netifaces \
    selenium paramiko

if [ $? -ne 0 ]; then
    echo "[!] Python module installation failed."
    exit 1
fi

echo "[*] All dependencies installed successfully."
echo "[*] You can now run X-Vector Pro with: ./run.sh"
