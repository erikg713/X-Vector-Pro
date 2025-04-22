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

```bash
git clone https://github.com/your-username/x-vector-pro.git
cd x-vector-pro
pip install -r requirements.txt
python main.py

## File Structure

x_vector_pro/
├── main.py                    # GUI Entrypoint
│
├── ui/                        # GUI interface
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

