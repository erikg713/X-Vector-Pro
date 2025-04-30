# X-Vector Pro


██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░

**Silent. Adaptive. Lethal.**  
X-Vector Pro is a tactical GUI-based WordPress attack suite. It automates the full penetration lifecycle with modules for recon, scanning, brute-force, CVE discovery, and exploit deployment.

---

## Features

- **Full Auto Mode** (Recon → Scan → Plugin Check → Exploit)
- **WordPress Brute Force** (via `xmlrpc.php`)
- **CVE Detection** using local `cve_db.json`
- **Plugin & Theme Enumeration**
- **Custom Exploit Runner** from the `exploits/` directory
- **CustomTkinter GUI Tabs** for modular navigation
- **Logs, Findings, and HTML Reports** for evidence & export

---

## Tech Stack

- Python 3.9+
- CustomTkinter
- Requests, TLDExtract
- XML-RPC, Regex, JSON, Sockets
- Threading, Importlib

---

## Getting Started

╭━╮╭━╮╭╮╱╱╭╮╱╱╱╱╭╮╱╱╱╱╱╱╱╭━━━╮
╰╮╰╯╭╯┃╰╮╭╯┃╱╱╱╭╯╰╮╱╱╱╱╱╱┃╭━╮┃
╱╰╮╭╯╱╰╮┃┃╭┻━┳━┻╮╭╋━━┳━╮╱┃╰━╯┣━┳━━╮
╱╭╯╰┳━━┫╰╯┃┃━┫╭━┫┃┃╭╮┃╭┻━┫╭━━┫╭┫╭╮┃
╭╯╭╮╰┳━┻╮╭┫┃━┫╰━┫╰┫╰╯┃┣━━┫┃╱╱┃┃┃╰╯┃
╰━╯╰━╯╱╱╰╯╰━━┻━━┻━┻━━┻╯╱╱╰╯╱╱╰╯╰━━╯
```bash
git clone https://github.com/your-username/x-vector-pro.git
cd x-vector-pro
pip install -r requirements.txt
python main.py

## File Structure

x_vector_pro/
├── main.py                    # GUI Entrypoint
│
├── gui/                        # GUI interface
│   ├── main_ui.py             # Launch & layout
│   ├── tabs/                  # Each tab is a GUI page
│   │   ├── auto_mode_tab.py
│   │   ├── scan_tab.py
│   │   ├── brute_tab.py
│   │   ├── cve_tab.py
│   │   ├── exploits_tab.py
│   │   ├── report_tab.py
│   │   └── settings_tab.py
│   └── components/            # Shared widgets
│       ├── logger_widget.py
│       └── form_inputs.py
│
├── engine/                    # Backend logic for each operation
│   ├── recon.py               # Domain analysis
│   ├── scanner.py             # Plugin & theme path checker
│   ├── cve_scanner.py         # Local CVE lookup engine
│   ├── brute_engine.py        # XML-RPC brute force logic
│   ├── exploit_runner.py      # Dynamic exploit loader
│   ├── auto_mode.py           # Orchestration pipeline
│   └── threading_manager.py   # Threaded execution manager
│
├── exploits/                  # Custom modular scripts (CVE-*.py)
│   └── README.md
│
├── utils/                     # Shared utilities
│   ├── logger.py
│   ├── net_helpers.py
│   ├── file_ops.py
│   └── validators.py
│
├── data/                      # Wordlists, config, CVEs
│   ├── cve_db.json
│   ├── wordlist.txt
│   ├── config.json
│   └── targets.txt
│
├── reports/                   # Auto-generated logs & reports
│   └── *.html / *.log
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

xvector_pro/
├── core/
│   ├── __init__.py
│   ├── brute_force.py
│   ├── recon.py
│   ├── scanner.py
│   ├── exploits/
│   │   ├── __init__.py
│   │   ├── exploit_ftp_backdoor.py
│   │   ├── exploit_sql_injection.py
│   │   └── ... (more exploits)
│   └── utils.py  # helpers like logging, proxies, encryption
│
├── gui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── auto_mode_tab.py
│   ├── brute_tab.py
│   ├── exploits_tab.py
│   ├── reports_tab.py
│   └── settings_tab.py
│
├── wordlists/
│   ├── passwords.txt
│   ├── usernames.txt
│   └── custom/
│       └── special_lists.txt
│
├── logs/
│   └── xvector_log.txt
│
├── reports/
│   └── recon_results/
│
├── config.json   # settings (threads, timeouts, proxies, etc.)
├── main.py       # main GUI launcher
├── README.txt
└── requirements.txt

X_Vector_Pro/
│
├── Main.py                  # Entry point
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/
│   ├── themes/
│   └── resources/
│
├── engine/                  # Main engine logic
│   ├── __init__.py
│   ├── controller.py
│   ├── scheduler.py
│   └── plugin_manager.py
│
├── core/                    # Core libraries/utilities
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   └── utils.py
│
├── scanner/                 # Scanning modules
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── vuln_scanner.py
│   └── service_scanner.py
│
├── brute/                   # Brute-forcing modules
│   ├── __init__.py
│   ├── password_brute.py
│   ├── username_enum.py
│   └── wordlists/
│
├── exploits/                # Exploit modules
│   ├── __init__.py
│   ├── exploit_base.py
│   ├── cve2025_1234.py
│   └── ...
│
├── recon/                   # Reconnaissance modules
│   ├── __init__.py
│   ├── subdomain_enum.py
│   ├── whois_lookup.py
│   └── passive_dns.py
│
├── report/                  # Reporting modules
│   ├── __init__.py
│   ├── html_report.py
│   ├── pdf_report.py
│   └── templates/
│
├── stealth/                 # Stealth/anti-detection modules
│   ├── __init__.py
│   ├── traffic_obfuscation.py
│   ├── user_agent_rotator.py
│   └── timing_attack.py
│
├── data/                    # Static data, wordlists, etc.
│   ├── fingerprints/
│   ├── payloads/
│   └── ...
│
├── docs/                    # Documentation
│   ├── README.md
│   └── usage.md
│
└── requirements.txt         # Dependencies

X_Vector_Pro/
│
├── Main.py                  # Entry point
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/
│   ├── themes/
│   └── resources/
│
├── engine/                  # Main engine logic
│   ├── __init__.py
│   ├── controller.py
│   ├── scheduler.py
│   └── plugin_manager.py
│
├── core/                    # Core libraries/utilities
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   └── utils.py
│
├── scanner/                 # Scanning modules
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── vuln_scanner.py
│   └── service_scanner.py
│
├── brute/                   # Brute-forcing modules
│   ├── __init__.py
│   ├── password_brute.py
│   ├── username_enum.py
│   └── wordlists/
│
├── exploits/                # Exploit modules
│   ├── __init__.py
│   ├── exploit_base.py
│   ├── cve2025_1234.py
│   └── ...
│
├── recon/                   # Reconnaissance modules
│   ├── __init__.py
│   ├── subdomain_enum.py
│   ├── whois_lookup.py
│   └── passive_dns.py
│
├── report/                  # Reporting modules
│   ├── __init__.py
│   ├── html_report.py
│   ├── pdf_report.py
│   └── templates/
│
├── stealth/                 # Stealth/anti-detection modules
│   ├── __init__.py
│   ├── traffic_obfuscation.py
│   ├── user_agent_rotator.py
│   └── timing_attack.py
│
├── data/                    # Static data, wordlists, etc.
│   ├── fingerprints/
│   ├── payloads/
│   └── ...
│
├── docs/                    # Documentation
│   ├── README.md
│   └── usage.md
│
└── requirements.txt         # Dependencies

██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░X_Vector_Pro/
│
├── Main.py                  # Entry point
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/
│   ├── themes/
│   └── resources/
│
├── engine/                  # Main engine logic
│   ├── __init__.py
│   ├── controller.py
│   ├── scheduler.py
│   └── plugin_manager.py
│
├── core/                    # Core libraries/utilities
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   └── utils.py
│
├── scanner/                 # Scanning modules
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── vuln_scanner.py
│   └── service_scanner.py
│
├── brute/                   # Brute-forcing modules
│   ├── __init__.py
│   ├── password_brute.py
│   ├── username_enum.py
│   └── wordlists/
│
├── exploits/                # Exploit modules
│   ├── __init__.py
│   ├── exploit_base.py
│   ├── cve2025_1234.py
│   └── ...
│
├── recon/                   # Reconnaissance modules
│   ├── __init__.py
│   ├── subdomain_enum.py
│   ├── whois_lookup.py
│   └── passive_dns.py
│
├── report/                  # Reporting modules
│   ├── __init__.py
│   ├── html_report.py
│   ├── pdf_report.py
│   └── templates/
│
├── stealth/                 # Stealth/anti-detection modules
│   ├── __init__.py
│   ├── traffic_obfuscation.py
│   ├── user_agent_rotator.py
│   └── timing_attack.py
│
├── data/                    # Static data, wordlists, etc.
│   ├── fingerprints/
│   ├── payloads/
│   └── ...
│
├── docs/                    # Documentation
│   ├── README.md
│   └── usage.md
│
└── requirements.txt         # Dependencies

▀▄▀ ▄▄ █░█ █▀▀ █▀▀ ▀█▀ █▀█ █▀█ ▄▄ █▀█ █▀█ █▀█
█░█ ░░ ▀▄▀ ██▄ █▄▄ ░█░ █▄█ █▀▄ ░░ █▀▀ █▀▄ █▄█X_Vector_Pro/
│
├── Main.py                  # Entry point
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── main_window.py
│   ├── widgets/
│   ├── themes/
│   └── resources/
│
├── engine/                  # Main engine logic
│   ├── __init__.py
│   ├── controller.py
│   ├── scheduler.py
│   └── plugin_manager.py
│
├── core/                    # Core libraries/utilities
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   └── utils.py
│
├── scanner/                 # Scanning modules
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── vuln_scanner.py
│   └── service_scanner.py
│
├── brute/                   # Brute-forcing modules
│   ├── __init__.py
│   ├── password_brute.py
│   ├── username_enum.py
│   └── wordlists/
│
├── exploits/                # Exploit modules
│   ├── __init__.py
│   ├── exploit_base.py
│   ├── cve2025_1234.py
│   └── ...
│
├── recon/                   # Reconnaissance modules
│   ├── __init__.py
│   ├── subdomain_enum.py
│   ├── whois_lookup.py
│   └── passive_dns.py
│
├── report/                  # Reporting modules
│   ├── __init__.py
│   ├── html_report.py
│   ├── pdf_report.py
│   └── templates/
│
├── stealth/                 # Stealth/anti-detection modules
│   ├── __init__.py
│   ├── traffic_obfuscation.py
│   ├── user_agent_rotator.py
│   └── timing_attack.py
│
├── data/                    # Static data, wordlists, etc.
│   ├── fingerprints/
│   ├── payloads/
│   └── ...
│
├── docs/                    # Documentation
│   ├── README.md
│   └── usage.md
│
└── requirements.txt         # Dependencies

