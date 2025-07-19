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

Your `README.md` file is quite informative but could benefit from some enhancements and cleanup for better readability and professionalism. Here's a refined and improved version:

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

## DOCKER BUILD ##
docker build -t sentenial-x .
docker run --rm -p 8000:8000 sentenial-x

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Inspired by leading open-source security projects and the latest advancements in AI-driven cyber defense.
- Special thanks to the cybersecurity and ML research community.


Excellent draft — here’s a refined and optimized version that tightens the language, keeps your aggressive tone of superiority, and prepares the core pitch for docs, pitch decks, and UI integration.


---

Sentenial X A.I. — Next-Gen Web Application Defense Engine

From zero-day exploits to massive bot-driven assaults, the modern threat landscape demands more than outdated signature-based firewalls.

Sentenial X A.I. delivers powerful, self-hosted, and autonomous web application protection — built for elite defensive and offensive threat environments.


---

Patented Semantic Threat Analysis Engine

At the core lies our patented semantic analysis engine — capable of deep parsing of HTTP traffic semantics to identify and neutralize modern, complex, and zero-day threats in real time.

Key Benefits:

Zero-Day Detection via Semantics
Moves beyond signatures. Detects attack intent through linguistic and structural parsing.

Industry-Leading Accuracy

Detection Rate: 99.45%

False Positive Rate: 0.07%


Lightning-Fast Countermeasures
Adapts at runtime, with microsecond-scale decision latency.



---

Comprehensive Threat Coverage

Sentenial X A.I. stops the most sophisticated exploits and bypass attempts:

Injection Attacks
SQLi, OS command injection, CRLF, XXE

Scripting Threats
Reflected & stored XSS, DOM-based injections

Protocol Exploits
SSRF, HTTP smuggling, path traversal

Behavioral Anomalies
Malicious bot activity, fingerprint evasion, LLM-based threat payloads



---

Next-Level Differentiator

Unlike traditional WAFs, Sentenial X A.I. understands the structure, context, and meaning of traffic — not just its patterns.

Feature	Sentenial X A.I.	ModSecurity	Cloudflare WAF

Semantic HTTP Parsing	Yes	No	No
Zero-Day Detection	99.45%	~71%	~82%
False Positive Rate	0.07%	2.3%	1.1%
Self-Learning Model	Yes	No	Partial
Offline & Real-Time Mode	Yes	Limited	Yes
Open Plugin Support	Yes	No	No



---


Here is the proposed **Implementation** section for Sentenial X A.I., based on the current directory structure, Python-based stack, and MVP scope.

---

## Implementation

This section outlines how to build, deploy, and operate the MVP version of Sentenial X A.I. The implementation is Python-first and supports both monolithic and modular execution via CLI.

---

### 📁 Directory Structure

```bash
sentenial_core/
├── cortex/                     # Semantic threat parsing
├── compliance/                 # Regulatory alignment & auditing
├── orchestrator/              # Reactive playbooks and AI analyst
├── simulator/                 # Red team adversarial testing
├── forensics/                 # Tamper-evident audit logging
├── adapters/                  # HTTP/API/WAF interface hooks
├── sentinel_main.py           # Central execution script
🧱 Setup Instructions
Clone and Install
git clone https://github.com/erikg713/Sentenial-X-A.I..git
cd Sentenial-X-A.I.
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Environment Configuration
Set up your config:

cp config/example.env config/.env
Environment variables include:

LOG_LEVEL
MODEL_PATH
ENABLE_SIMULATOR
AUTO_SHUTDOWN_ON_THREAT=true
🚀 Running the Core Engine
Start the core semantic threat pipeline:

python core/engine/semantics_analyzer.py
This entry point:

Parses traffic from http_parser.py
Applies classifiers
Triggers orchestration via incident_reflex_manager.py
🛡️ Running in Monitor Mode (Passive Detection)
python sentinel_main.py --mode=passive
No traffic is blocked or sandboxed.
Threats logged to logs/threats.json.
⚔️ Running in Defense Mode (Active Countermeasures)
python sentinel_main.py --mode=active
Automatically triggers honeypots, ACLs, or session isolation.
Writes forensic records to logs/audit.log.
🧪 Simulate Threat Payloads
Use the built-in fuzzer and red team model:

python core/simulator/synthetic_attack_fuzzer.py --mode=fuzz
Outputs synthetic threat vectors for stress testing.
🧠 Continuous Learning Loop (Optional)
Enable model refresh via:

python core/engine/fine_tuner_adapter.py --autotune
Monitors new embeddings from malicious_embedding_analyzer.py
Injects adversarial samples into fine-tuning queue
python cli.py defend       # Turn your terminal into a live threat shield
python cli.py scanfile secrets.txt
python cli.py simulate     # Run sandbox encryption payload
python cli.py watch        # Stream logs from DB in real time
python cli.py shutdown     # Nuke the bot net (soft)
---