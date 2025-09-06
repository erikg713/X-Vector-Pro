### 📘 README.md ###

# X-Vector Pro

---------------------------------------------------------
██╗░░██╗░░░░░░██╗░░░██╗███████╗░█████╗░████████╗  
╚██╗██╔╝░░░░░░██║░░░██║██╔════╝██╔══██╗╚══██╔══╝  
░╚███╔╝░█████╗╚██╗░██╔╝█████╗░░██║░░╚═╝░░░██║░░░  
░██╔██╗░╚════╝░╚████╔╝░██╔══╝░░██║░░██╗░░░██║░░░  
██╔╝╚██╗░░░░░░░░╚██╔╝░░███████╗╚█████╔╝░░░██║░░░  
╚═╝░░╚═╝░░░░░░░░░╚═╝░░░╚══════╝░╚════╝░░░░╚═╝░░░  
----------------------------------------------------------

[![Build](https://img.shields.io/github/actions/workflow/status/erikg713/X-Vector-Pro-GUI-Tool/ci.yml?branch=main)](https://github.com/erikg713/X-Vector-Pro-GUI-Tool/actions)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://erikg713.github.io/X-Vector-Pro-GUI-Tool/)
[![License](https://img.shields.io/github/license/erikg713/X-Vector-Pro-GUI-Tool)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

**Silent. Adaptive. Modular.**  
X-Vector Pro is a tactical, GUI-based assessment toolkit with both **graphical** and **CLI** workflows.

---

## 🚀 Why X-Vector Pro?

- Unified **GUI + CLI** workflow  
- Modular architecture (Recon, Scan, Analysis, Reports)  
- Extensible exploit and plugin system  
- Generates **HTML/PDF reports** for documentation  
- Built with contributors in mind (PEP-8, testing, CI/CD)

---

## 📦 Quick Start

Clone and launch:

```bash
git clone https://github.com/erikg713/X-Vector-Pro-GUI-Tool.git
cd X-Vector-Pro-GUI-Tool
pip install -r requirements.txt
python main.py


---

⚡ CLI Usage

Flag	Description

--auto	Run full pipeline (Recon → Scan → Analysis)
--target URL	Specify target (e.g. https://demo.site)
--scan-plugins	Enumerate installed plugins and themes
--cve-check	Check against local data/cve_db.json
--report-dir	Output directory for logs & reports


Example:

python main.py --auto --target https://demo.site --report-dir reports/$(date +%Y%m%d)


---

📊 Features

Full Auto Mode – end-to-end assessment pipeline

GUI Interface – CustomTkinter dashboard

Reports – exportable HTML/PDF with findings

Extensible – drop-in modules for new features



---

🏗 Architecture

flowchart LR
  GUI[GUI Tabs] --> Controller
  CLI[CLI Parser] --> Controller
  Controller --> Recon
  Controller --> Scan
  Controller --> CVE
  Controller --> Reports

See full breakdown in docs/architecture.md.


---

📚 Documentation

Built with MkDocs + Material

Live docs: 📖 X-Vector Pro Docs


Local build:

pip install mkdocs-material
mkdocs serve


---

🤝 Contributing

We welcome contributions!

Follow PEP-8 (≤79 chars/line).

Add tests (pytest) with ≥80% coverage.

Use core/logger.py (no raw print).

Submit PR → CI runs lint, tests, docs build.


See docs/developer_guide.md for full guide.


---

🗺 Roadmap

Plugin system for custom detection modules

Expanded API and integrations

Advanced reporting & analytics dashboard

Community-driven exploit/scan library



---

📄 License

This project is licensed under the MIT License. See LICENSE for details.

---

# ✅ Docs Additions

- Add `docs/quickstart.md` (step-by-step install + screenshots).  
- Add `docs/faq.md` (common Q&A).  
- Add `docs/contributing.md` (contributor checklist).  
- Enhance `mkdocs.yml` navigation:

```yaml
nav:
  - Home: index.md
  - Quick Start: quickstart.md
  - Usage: usage.md
  - Architecture: architecture.md
  - Developer Guide: developer_guide.md
  - FAQ: faq.md
  - Contributing: contributing.md


---
