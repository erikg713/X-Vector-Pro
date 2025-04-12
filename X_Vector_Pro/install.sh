#!/bin/bash
echo "[*] Installing X-Vector Pro dependencies..."
sudo apt update
sudo apt install python3-tk -y
pip install requests customtkinter tldextract
echo "[*] Done. Run with: ./run.sh"
