![X-Vector Pro Screenshot](docs/screenshot-dark.png)
![X-Vector Pro Auto Mode Demo](docs/demo-auto-mode.gif)
---

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

## Screenshots

Coming Soon – GUI preview image

---

## Authors

Built with dedication and expertise by **Erik G.**

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
