## README.md ##

```markdown
# X-Vector Pro
---------------------------------------------------------
██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗  
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝  
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░  
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░  
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░  
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░  
----------------------------------------------------------
**Silent. Adaptive. Lethal.**  
Tactical GUI-based WordPress attack suite automating recon, scanning, brute-force, CVE discovery, and exploits.

---

## Table of Contents

1. [Quick Start](#quick-start)  
2. [Features & Examples](#features--examples)  
3. [Architecture](#architecture)  
4. [Documentation Site](#documentation-site)  
5. [Contributing & Developer Guide](#contributing--developer-guide)  
6. [Roadmap](#roadmap)  
7. [License](#license)  

---

## Quick Start

Clone and launch:

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py
```

CLI flags:

| Flag            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| `--auto`        | Run full pipeline (Recon → Scan → Plugins → Exploits)      |
| `--target URL`  | Specify WordPress site (e.g. `https://vuln.site`)         |
| `--scan-plugins`| Enumerate installed plugins and versions                  |
| `--cve-check`   | Detect local CVEs from `data/cve_db.json`                 |
| `--report-dir`  | Custom output directory for logs & HTML reports           |

Generate an HTML report:

```bash
python main.py --auto --target https://testwp.local --report-dir reports/$(date +%Y%m%d)
```

---

## Features & Examples

### Full Auto Mode

Kick off end-to-end assessment:

```bash
python main.py --auto --target https://example.com
```

### WordPress Brute-Force

```python
from brute.password_brute import BruteEngine

engine = BruteEngine(target="https://site.local/xmlrpc.php")
engine.load_wordlist("data/wordlists/passwords.txt")
engine.start()
```

### CVE Detection & Enumeration

```bash
python main.py --cve-check --target https://vuln.site
```

Outputs discovered CVEs in console and `reports/`.

### Plugin & Theme Scan

```bash
python main.py --scan-plugins --target https://demo.wp
```

Flags outdated components for further action.
pytest tests/test_tor_detector.py

---

## Architecture

Core layers and data-flow:

```
       +-----------+       +-----------+
       |  GUI Tab  |       |   CLI     |
       +-----+-----+       +-----+-----+
             |                   |
             v                   v
    +--------+--------+ +--------+--------+
    |   Controller    | |  ArgParser/CLI  |
    +--------+--------+ +--------+--------+
             |                   |
+------------+------------+      |
| Recon | Scan | Brute | CVE |   |
+------------+------------+      |
             |                   |
         +---+---+           +---+---+
         | Exploit |-------->| Reports|
         +--------+           +-------+
```

See full breakdown in [`docs/architecture.md`](docs/architecture.md).

---

## Documentation Site

We use **MkDocs + Material** theme.  

**mkdocs.yml**:

```yaml
site_name: X-Vector Pro Docs
nav:
  - Home: index.md
  - Usage: usage.md
  - Architecture: architecture.md
  - Developer Guide: developer_guide.md
theme:
  name: material
markdown_extensions:
  - toc:
      permalink: true
```

Build & preview locally:

```bash
pip install mkdocs-material
mkdocs serve
```

---

## Contributing & Developer Guide

- Follow **PEP-8**: line width ≤79, snake_case, Google-style docstrings.  
- Logging via `core/logger.py`, avoid `print()`.  
- Unit tests in `tests/`, use `pytest` + `responses` for HTTP mocking.

### Adding a New Exploit Module

1. Create `exploits/CVEYYYY_NNNN.py`.  
2. Subclass `ExploitBase`:

   ```python
   class CVE2025_9999(ExploitBase):
       def check(self):
           # fingerprint logic
           ...
       def exploit(self):
           # payload delivery
           ...
   ```

3. Drop into `exploits/`; dynamic loader picks it up.

### Pull Request Workflow

1. Fork & branch off `main`.  
2. Add tests with ≥80% coverage.  
3. Submit PR—CI runs lint, tests, docs build.  

Full developer guide in [`docs/developer_guide.md`](docs/developer_guide.md).

---

## Roadmap

- Modular plugin system for custom threat detection  
- Fine-tuned organizational workflows  
- Expanded API & protocol adapters  
- Advanced analytics dashboard  

---

## License

This project is MIT-licensed. See `LICENSE` for details.
```

---

# mkdocs.yml

```yaml
site_name: X-Vector Pro Docs
nav:
  - Home: index.md
  - Usage: usage.md
  - Architecture: architecture.md
  - Developer Guide: developer_guide.md
theme:
  name: material
markdown_extensions:
  - toc:
      permalink: true
```

---

# /docs/index.md

```markdown
# X-Vector Pro Documentation

Welcome to the official docs for **X-Vector Pro**, a GUI-based WordPress attack suite.

X-Vector Pro automates:
- Reconnaissance
- Scanning & Enumeration
- Brute-force attacks
- CVE lookup
- Exploit deployment
- HTML report generation

Use the sidebar to explore setup, workflow examples, architecture details, and developer guidelines.
```

---

# /docs/usage.md

```markdown
# Usage & Examples

## Installation

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
```

## GUI Walkthrough

1. Launch `python main.py`.  
2. Select **Auto Mode** tab.  
3. Enter target URL and click **Start**.  
4. Watch progress logs, then export HTML/PDF report.

## CLI Examples

| Command                                                     | Effect                                                             |
| ----------------------------------------------------------- | ------------------------------------------------------------------ |
| `python main.py --auto --target https://example.com`         | Full pipeline from recon to exploit + report                       |
| `python main.py --scan-plugins --target https://demo.wp`     | Enumerate and version-check plugins/themes                         |
| `python main.py --cve-check --target https://vuln.site`      | Detect local CVEs and annotate results in reports                  |
| `python main.py --auto --target https://test --report-dir r` | Custom directory for saving logs & HTML report                     |
```

---

# /docs/architecture.md

```markdown
# Architecture Overview

X-Vector Pro is divided into modular layers:

```
       +-----------+       +-----------+
       |  GUI Tab  |       |   CLI     |
       +-----+-----+       +-----+-----+
             |                   |
             v                   v
    +--------+--------+ +--------+--------+
    |   Controller    | |  ArgParser/CLI  |
    +--------+--------+ +--------+--------+
             |                   |
+------------+------------+      |
| Recon | Scan | Brute | CVE |   |
+------------+------------+      |
             |                   |
         +---+---+           +---+---+
         | Exploit |-------->| Reports|
         +--------+           +-------+
```

## Layer Descriptions

- **GUI Layer**  
  CustomTkinter tabs for each feature.  
- **CLI Interface**  
  `argparse` parser supporting flags shown in Usage.  
- **Controller/Scheduler**  
  Orchestrates module execution, manages threading.  
- **Recon / Scan / Brute / CVE**  
  Individual modules under `/recon`, `/scanner`, `/brute`, `/core/cve_scanner.py`.  
- **Exploit Runner**  
  Dynamically loads `exploits/*` classes and executes them.  
- **Report Generator**  
  Builds HTML/PDF using Jinja2 templates in `/docs/templates`.

See code comments in `/engine/` for data-flow details.
```

---

# /docs/developer_guide.md

```markdown
# Developer Guide

Welcome, contributor! This guide covers coding standards, how to add modules, and testing workflows.

## Coding Standards

- Follow PEP-8: max 79-char lines, snake_case for funcs, PascalCase for classes.  
- Docstrings: use Google style.  
- Logging: use `core/logger.py` at appropriate levels; no `print()`.

## Adding a New Exploit

1. Create `exploits/CVEYYYY_NNNN.py`.  
2. Import and subclass:

   ```python
   from exploits.exploit_base import ExploitBase

   class CVE2025_9999(ExploitBase):
       def check(self):
           # Detect vulnerability
           ...
       def exploit(self):
           # Execute payload
           ...
   ```

3. No extra imports required—dynamic loader autodiscovers.

## Testing

- Tests live in `tests/` mirroring module structure.  
- Use `pytest` and `responses` for HTTP mocks.  
- GUI: stub with `pytest-qt` or `unittest.mock`.

Example test:

```python
def test_recon_subdomain_enum(monkeypatch):
    from recon.subdomain_enum import SubdomainEnum
    monkeypatch.setattr('requests.get', lambda *a, **k: DummyResponse(...))
    se = SubdomainEnum(target="example.com")
    assert "sub.example.com" in se.run()
```

## CI & Workflow

1. Fork & PR against `main`.  
2. Ensure ≥80% coverage.  
3. PR triggers GitHub Actions: lint, pytest, mkdocs build.  
4. Merge upon green checks.

Thank you for helping X-Vector Pro evolve!
```

---

Copy these files into your repo, install `mkdocs-material`, and you’ll have a complete, polished documentation suite. Let me know if you need screenshots embedded or any further tweaks!
