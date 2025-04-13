

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
├── main.py                           # Entry point for GUI launcher
├── config.json                       # App-wide configuration (JSON-based)
├── .env                              # Secrets, API keys, or paths (optional)
├── README.txt
├── requirements.txt

├── logs/                             # Organized event & tool output
│   ├── pcaps/                        # Wireshark-ready .pcap captures
│   ├── reports/                      # Saved recon/brute reports
│   ├── activity/                     # Internal logs + user actions
│   └── ids/                          # Suricata raw logs

├── wordlists/                        # Custom or imported wordlists
│   ├── ssh.txt
│   ├── web_fuzz.txt
│   └── user_agents.txt

├── exploits/                         # Modular exploit scripts
│   ├── cve2024_xxx.py
│   ├── metasploit_adapter.py
│   └── exploit_base.py

├── reports/                          # Export tools
│   ├── exporter.py                   # PDF/HTML/JSON conversion
│   └── templates/                    # Report templates (HTML/Jinja)

├── gui/                              # GUI Layer (CustomTkinter)
│   ├── dashboard.py                  # Central window controller
│   └── tabs/                         # Tabs for each functional module
│       ├── recon_tab.py
│       ├── brute_tab.py
│       ├── scanner_tab.py
│       ├── ids_tab.py
│       ├── exploit_tab.py
│       └── auto_mode_tab.py

├── core/                             # Backend engines
│   ├── auto_mode/
│   │   └── sequencer.py              # Full automation chain
│   ├── brute_force/
│   │   ├── ssh_brute.py
│   │   └── ftp_brute.py
│   ├── recon/
│   │   ├── recon_engine.py
│   │   └── dns_enum.py
│   ├── scanner/
│   │   ├── port_scanner.py
│   │   └── vuln_scanner.py
│   ├── controller/
│   │   └── master_control.py
│   ├── ids/
│   │   ├── suricata_manager.py
│   │   ├── log_parser.py
│   │   ├── auto_analyzer.py
│   │   └── packet_capture.py
│   ├── plugins/                      # Optional tools or extensions
│   │   ├── mitm_proxy.py
│   │   └── custom_payloads.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── helpers.py
│   │   └── timer.py
│   └── __init__.py

├── tests/                            # Unit + integration tests
│   ├── test_recon.py
│   ├── test_brute.py
│   └── test_exploits.py

└── setup.py                          # For packaging as a Python tool or .exe
