````markdown
# ███╗   ██╗██╗   ██╗██╗  ██╗██╗   ██╗███████╗████████╗███████╗██████╗ 
# ████╗  ██║██║   ██║██║ ██╔╝██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
# ██╔██╗ ██║██║   ██║█████╔╝ ██║   ██║█████╗     ██║   █████╗  ██████╔╝
# ██║╚██╗██║██║   ██║██╔═██╗ ██║   ██║██╔══╝     ██║   ██╔══╝  ██╔══██╗
# ██║ ╚████║╚██████╔╝██║  ██╗╚██████╔╝███████╗   ██║   ███████╗██║  ██║
# ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
# ============================================================================
#                    X-VECTOR PRO – RED TEAM WORDPRESS SUITE
# ============================================================================

**Silent. Adaptive. Lethal.**  
A GUI-based, modular WordPress exploitation and threat automation platform built for red teams, security researchers, and adversary simulation units.

> 🎯 Automates reconnaissance, vulnerability analysis, CVE sync, credential brute-forcing, plugin enumeration, and real-time auto-exploitation in a persistent, stealth-oriented background workflow.

---

## ⚠️ Legal & Ethical Notice

**X-Vector Pro is built for professional use only.**  
You are solely responsible for any use of this tool. Unauthorized access or attacks on systems you do not own or have explicit permission to test is illegal and unethical.

---

## 🧠 Core Features

- 🔁 **Continuous Recon Mode**: Background fingerprinting, passive DNS, CDN/CDN bypass attempts, and port probing  
- ⚙️ **CVE-Aware Scanning**: Local + synced CVE detection with automatic matching to vulnerable versions of themes/plugins  
- 🔓 **Brute Engine**: Multi-threaded login brute-force via XML-RPC and `/wp-login.php` endpoints  
- 🛠️ **Exploit Execution**: Modular payload runner supporting CVEs and post-exploitation modules  
- 📡 **Live Threat Sync**: Auto-fetch CVEs and plugin/theme zero-days from curated threat feeds  
- 🧩 **Plugin/Theme Enumeration**: Full version fingerprinting, CVSS scoring, and outdated version detection  
- 📋 **Automated Reporting**: Generates timestamped HTML/PDF reports for engagements  
- 💻 **GUI & CLI Hybrid**: Operate via simple GUI or full headless CLI automation

---

## 🚀 Quickstart (Red Team Mode)

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py --auto --target "https://targetsite.tld"
````

### Command Breakdown:

| Flag             | Description                                   |
| ---------------- | --------------------------------------------- |
| `--auto`         | Full-stack recon → scan → CVE match → exploit |
| `--target`       | Target WordPress site                         |
| `--cve-sync`     | Pull latest CVE data to local DB              |
| `--persist`      | Run silently in background mode               |
| `--scan-plugins` | Only enumerate plugins/themes                 |
| `--brute`        | Run brute-force on login or XML-RPC           |

### GUI Mode

```bash
python main.py
```

* Navigate to "Auto Mode"
* Enter target URL
* Watch the chain of execution via GUI logs

---

## 📡 CVE Sync & Threat Intelligence

X-Vector auto-syncs public and private vulnerability feeds:

* \[✔] **National Vulnerability Database (NVD)**
* \[✔] **WPVulnDB**
* \[✔] **ExploitDB CVEs**
* \[✔] **0day.today (if key provided)**
* \[✔] **Custom GitHub CVE mirrors**

### Manual Sync:

```bash
python main.py --cve-sync
```

Stores structured data in `data/cve_db.json`, auto-linked during scans by plugin/theme slug, version, or known hashes.

---

## 🧱 Architecture

```
       +---------------------+
       |     GUI / CLI       |
       +----------+----------+
                  |
         +--------v--------+
         |   Core Engine   |
         +--------+--------+
                  |
   +--------------+--------------+
   |      Recon + Fingerprint    |
   |      Brute Force Engine     |
   |      Plugin/Theme Scanner   |
   |      CVE Detector/Matcher   |
   |      Exploit Runner         |
   +--------------+--------------+
                  |
           +------v------+
           | ReportGen    |
           +-------------+
```

---

## 🔧 Developer Guide

### Coding Standards

* **PEP8** compliance (line limit: 79 chars)
* Use `core/logger.py` for all logging
* `snake_case` for functions, `PascalCase` for classes
* Docstrings: Google-style

### Add Exploit Module

```python
# exploits/CVE2025_9999.py
from core.base import ExploitBase

class CVE2025_9999(ExploitBase):
    def check(self):
        # Check vulnerable conditions
        return self.target.has_plugin("vuln-plugin", version="<1.2.3")

    def exploit(self):
        # Deliver payload
        self.session.post(self.url + "/vuln-path", data={"cmd": "whoami"})
```

Register module automatically via dynamic import system.

---

## 🧪 Testing & CI/CD

* Tests live in `/tests/` per module
* Use `pytest` and `responses` for mocking web endpoints
* GUI tests with `pytest-qt`
* GitHub Actions CI runs:

  * Style checks
  * Unit tests
  * MkDocs build

---

## 📂 Documentation with MkDocs

```bash
pip install mkdocs-material
mkdocs serve     # Local preview
mkdocs build     # Static site → /site/
```

**Structure:**

```
mkdocs.yml
/docs/
  index.md
  usage.md
  modules.md
  dev_guide.md
  roadmap.md
```

---

## 📅 Roadmap

* ✅ Dynamic CVE sync & auto-matching engine
* ✅ Persistent background recon daemon
* ⏳ Live threat dashboards w/ CVSS heatmap
* ⏳ Multi-target swarm mode (horizontal org scan)
* ⏳ Plugin system for zero-day deployment modules
* ⏳ Webhook-based reporting into SIEM/Slack/Discord
* ⏳ API-first rewrite for integration into C2 frameworks

---

## 🧠 Use Cases

* Red Team WordPress assessments
* Adversary simulation on client environments
* Internal pen testing automation
* Purple team plugin and CVE behavior analysis
* Bug bounty WordPress recon/scanning pipelines

---

## 📜 License

MIT License. See [LICENSE](./LICENSE).

---

## 🤝 Contributing

1. Fork and create feature branch
2. Follow coding standards and write tests
3. Submit a PR with linked issue and description
4. Auto-CI will validate it on push

---

## 👣 Credits

* Built with ❤️ by @erikg713 and contributors
* Powered by Python, Qt5, and a healthy dose of paranoia

---

> “You won't see us coming. But your logs will remember.”

```
---
