-----------------------------
### X-Vector Pro ###
-----------------------------

▀▄▀ ▄▄ █░█ █▀▀ █▀▀ ▀█▀ █▀█ █▀█ ▄▄ █▀█ █▀█ █▀█
█░█ ░░ ▀▄▀ ██▄ █▄▄ ░█░ █▄█ █▀▄ ░░ █▀▀ █▀▄ █▄█

**Silent. Adaptive. Lethal.**  
Tactical GUI-based WordPress attack suite automating recon, scanning, brute-force, CVE discovery, and exploit deployment.

---

## Table of Contents

1. [Quick Start & Usage](#quick-start--usage)  
2. [Features & Examples](#features--examples)  
3. [Architecture Overview](#architecture-overview)  
4. [Project Documentation Site (MkDocs)](#project-documentation-site-mkdocs)  
5. [Developer Guidelines](#developer-guidelines)  
6. [Roadmap](#roadmap)  

---
---------------------------------------------------------

██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░
----------------------------------------------------------
---
## Quick Start & Usage ##

Clone the repo and install dependencies:

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py
```

Run Full Auto Mode against a target:

```bash
python main.py --auto --target “https://example.com”
```

Breakdown:

- `--auto` invokes Recon → Scan → Plugin Check → Exploit  
- `--target` specifies the WordPress site URL  
- Logs and HTML reports land in `reports/YYYYMMDD_HHMMSS/`

---

## Features & Examples

### 1. Full Auto Mode

Launch end-to-end workflow in one click:

```bash
# GUI: Auto Mode tab → Enter URL → Start
# CLI: 
python main.py --auto --target https://testwp.local
```

### 2. WordPress Brute Force

Via `xmlrpc.php` with custom wordlists:

```python
from brute.password_brute import BruteEngine

engine = BruteEngine(target="https://site.local/xmlrpc.php")
engine.load_wordlist("data/wordlists/passwords.txt")
engine.start()
```

### 3. CVE Detection

Local lookup using `cve_db.json`:

```bash
python main.py --cve-check --target https://vulnerable.site
```

List of detected CVEs outputs to console and embeds in HTML report.

### 4. Plugin & Theme Enumeration

```bash
python main.py --scan-plugins --target https://demo.wp
```

Outputs versions and flags any outdated components.

---

## Architecture Overview

This section maps key modules and data flows.

```
       +--------------+          +------------------+
       |   GUI Layer  |          |   CLI Interface  |
       +------+-------+          +----------+-------+
              |                           |
              | user action               | flags & args
              v                           v
       +------+---------------------------+------+
       |          Controller / Scheduler        |
       +------+---------------------------+------+
              |                           |
   +----------+----------+      +---------+--------+
   |    Recon Module     |      |    Scanner       |
   +----------+----------+      +---------+--------+
              |                           |
   +----------+----------+      +---------+--------+
   |    Brute Engine     |      |  CVE Scanner      |
   +----------+----------+      +---------+--------+
              \                           /
               \                         /
                +------------+----------+
                             |
                   +---------+--------+
                   |   Exploit Runner  |
                   +-------------------+
                             |
                   +---------+---------+
                   |   Report Generator |
                   +--------------------+
```

Data flows from user input through orchestrator, then through recon/scanning/bruting/CVE, culminating in exploit execution and report generation.

---

## Project Documentation Site (MkDocs)

Proposed structure:

```
mkdocs.yml
/docs
  index.md
  usage.md
  architecture.md
  developer_guide.md
```

`mkdocs.yml`:

```yaml
site_name: X-Vector Pro Docs
nav:
  - Home: index.md
  - Usage: usage.md
  - Architecture: architecture.md
  - Developer Guide: developer_guide.md
theme:
  name: material
```

Create each markdown under `/docs/`:

- **index.md**: Project intro and features  
- **usage.md**: Quick start snippets, CLI flags, GUI walkthrough  
- **architecture.md**: ASCII/diagram, module descriptions  
- **developer_guide.md**: Coding standards, module extension, testing  

Build site:

```bash
pip install mkdocs-material
mkdocs serve       # for local preview
mkdocs build       # output to site/
```

---

## Developer Guidelines

### Coding Standards

- Follow PEP8: 79-char line width, snake_case for functions, PascalCase for classes.  
- Docstrings: use Google style for all public methods.  
- Logging: leverage `core/logger.py` at INFO/DEBUG levels; avoid print statements.

### Adding a New Exploit Module

1. Create `exploits/CVEYYYY_NNNN.py`.  
2. Inherit from `ExploitBase` and implement:
   ```python
   class CVE2025_9999(ExploitBase):
       def check(self):    # fingerprint target
           ...
       def exploit(self):  # deliver payload
           ...
   ```
3. Update `exploits/__init__.py` if using manual import (dynamic import covers most cases).

### Testing Tips

- Unit tests live in `tests/` alongside each module.  
- Use pytest fixtures to simulate HTTP endpoints via `responses` library.  
- For GUI elements, use `pytest-qt` or `unittest.mock` to stub button callbacks.

### Workflow for Contributions

1. Fork repo & create feature branch.  
2. Write tests—ensure 80%+ coverage.  
3. Submit PR with descriptive title and linked issue.  
4. CI runs lint, tests, and builds docs automatically.  

---

## Roadmap

- Modular plugin system for custom threat detection  
- Fine-tuning workflows for organizational threat patterns  
- Expanded API and protocol adapters  
- Advanced analytics dashboard  

Looking forward to your feedback and contributions!
