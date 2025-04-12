

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
├── main.py                         ← GUI Launcher (non-blocking)
├── core/
│   ├── __init__.py
│   ├── controller.py               ← Threaded task manager, orchestrates modules
│   ├── brute.py                    ← Optimized XML-RPC brute module
│   ├── recon.py                    ← Recon module (CMS, headers, IP)
│   ├── scanner.py                  ← DirBuster + port scanner
│   └── report.py                   ← HTML report writer
│
├── exploits/                       ← Dynamically loaded exploit modules
│   ├── __init__.py
│   └── revslider_upload_rce.py    ← Sample plugin exploit
│
├── gui/
│   ├── __init__.py
│   └── dashboard.py               ← CustomTkinter GUI (modular + threaded)
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                  ← Asynchronous logger
│   └── xmlrpc_utils.py            ← system.multicall, payload builder
│
├── wordlists/
│   └── rockyou.txt                ← Default wordlist (line-by-line read)
│
├── config.json                    ← Editable settings
├── cve_db.json                    ← CVE mapping for plugins/themes
├── xvector_log.txt                ← Runtime logs
├── xvector_report.html            ← Generated report
├── icon.ico                       ← Windows app icon
├── run.sh                         ← Linux/macOS launcher
├── install.sh                     ← Dependency installer
└── README.txt                     ← Instructions
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

X-Vector Pro: WordPress Recon & Exploit Suite

1. Requirements:
   - Python 3.8+
   - pip install customtkinter requests tldextract pyinstaller

2. Run:
   python main.py

3. Modules:
   - Recon: CMS, IP, Headers, Subdomains
   - Scanner: Ports + DirBuster
   - Brute: XML-RPC login
   - Exploits: Plugin RCEs (via CVE match)
   - Full Auto: One-click attack chain

4. Customize:
   - Add your own exploits in /exploits/
   - Add CVEs in cve_db.json
   - Update wordlist path in config.json
