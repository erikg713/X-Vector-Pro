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



▀▄▀ ▄▄ █░█ █▀▀ █▀▀ ▀█▀ █▀█ █▀█ ▄▄ █▀█ █▀█ █▀█
█░█ ░░ ▀▄▀ ██▄ █▄▄ ░█░ █▄█ █▀▄ ░░ █▀▀ █▀▄ █▄█

X-Vector-Pro/
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

# X-Vector Pro

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

Clone the repository and install the dependencies:

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py
```

---

## File Structure

```
x_vector_pro/
├── main.py                    # GUI Entrypoint
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
├── engine/                    # Backend logic for each operation
│   ├── recon.py               # Domain analysis
│   ├── scanner.py             # Plugin & theme path checker
│   ├── cve_scanner.py         # Local CVE lookup engine
│   ├── brute_engine.py        # XML-RPC brute force logic
│   ├── exploit_runner.py      # Dynamic exploit loader
│   ├── auto_mode.py           # Orchestration pipeline
│   └── threading_manager.py   # Threaded execution manager
├── exploits/                  # Custom modular scripts (CVE-*.py)
├── utils/                     # Shared utilities
├── data/                      # Wordlists, config, CVEs
├── reports/                   # Auto-generated logs & reports
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## Screenshots

+---------------------------------------------------------+
| Recon - Information Gathering                           |
|---------------------------------------------------------|
| [Target Input]         [ Start Recon ] [ Stop Recon ]   |
|                                                           |
| [ ] Reconnaissance                                        |
| [ ] Port Scanning                                         |
| [ ] Vulnerability Scan                                    |
| [ ] Web Brute Force                                       |
| [ ] Subdomain Enumeration                                 |
|                                                           |
| [Progress Bar]                                            |
|                                                           |
| [----------------- Live Logs Text Box ------------------] |
+---------------------------------------------------------+
| Settings | Reports | About                                |
+---------------------------------------------------------+

---

## Authors

Built with dedication and expertise by **Erik G.**

---

## License

This project is licensed under MIT

## Roadmap

- [ ] Modular plugin system for custom threat detection
- [ ] Fine-tuning workflows for organizational threat patterns
- [ ] Expanded API and protocol adapters
- [ ] Advanced analytics dashboard
---
