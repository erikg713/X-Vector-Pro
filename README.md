

### X-Vector Pro ###

A slick GUI tool to brute-force WordPress accounts via `xmlrpc.php`. Great for red teamers, CTFs, and penetration testers who like visuals with their exploits.

> Educational use only. Don't break into systems you don't own.

---

## Features

- GUI interface (Tkinter)
- Support multiple usernames
- Smart or custom wordlists
- `system.multicall` for stealthy login brute-forcing
- Logs valid credentials to `hits.txt`
- Cross-platform (Kali, Parrot, Ubuntu)

---

## How to Use

```bash
git clone https://github.com/YOUR_USERNAME/wp-xmlrpc-gui.git
cd wp-xmlrpc-gui
./install.sh

Then:

./run.sh


---

Screenshot




---

Authors

Built with blood, bytes & a keyboard by ERIK G.


---

---

### **2. `install.sh`**

```bash
#!/bin/bash
echo "[*] Installing WP XML-RPC GUI Brute Tool..."
sudo apt update
sudo apt install python3-tk -y

echo "[*] Done. You can now run the tool with:"
echo "./run.sh"


---

3. File Tree Structure

X-Vector-Pro/
│
├── main.py                     ← Main launcher GUI (core app)
├── config.json                 ← Settings file
├── cve_db.json                 ← Vulnerability database (plugin/theme CVEs)
├── xvector_log.txt             ← Generated logs (auto-created)
├── xvector_report.html         ← Optional HTML report (auto-created)
│
├── exploits/                   ← Exploit payload modules
│   ├── __init__.py
│   └── revslider_upload_rce.py
│
├── wordlists/                  ← Wordlists used in Brute/Dir scans
│   └── rockyou.txt             ← Default sample wordlist
│
├── icon.ico                    ← Optional icon for EXE
└── README.txt                  ← Basic instructions
---
### REQUIREMENTS ###
pip install requests tldextract
pip install customkinter
---

---

 ### Push to GitHub ###

cd ~/wp-xmlrpc-gui
git init
git add .
git commit -m "Initial Commit: WP XML-RPC GUI Brute Tool"
git remote add origin https://github.com/YOUR_USERNAME/wp-xmlrpc-gui.git
git branch -M main
git push -u origin main


---

