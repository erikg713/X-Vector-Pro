# Developer Guide #

Welcome, contributor! This guide covers coding standards, how to add modules, and testing workflows.

## Coding Standards

- Follow PEP-8: max 79-character lines, snake_case for functions, PascalCase for classes.  
- Docstrings: Google style.  
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

Layer Descriptions
GUI Layer CustomTkinter tabs for each feature.

CLI Interface argparse-based parser supporting the flags shown in Usage.

Controller/Scheduler Orchestrates module execution and manages threading.

Recon / Scan / Brute / CVE Individual modules under /recon, /scanner, /brute, /core/cve_scanner.py.

Exploit Runner Dynamically loads exploits/* classes and executes them.

Report Generator Builds HTML/PDF using Jinja2 templates in /docs/templates.


---

## docs/developer_guide.md

```markdown
# Developer Guide

Welcome, contributor! This guide covers coding standards, how to add modules, and testing workflows.

## Coding Standards

- Follow PEP-8: max 79-character lines, snake_case for functions, PascalCase for classes.  
- Docstrings: Google style.  
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
No extra imports required—dynamic loader autodiscovers.

Testing
Tests live in tests/ mirroring module structure.

Use pytest and responses for HTTP mocks.

GUI: stub with pytest-qt or unittest.mock.

Example test:

python
def test_recon_subdomain_enum(monkeypatch):
    from recon.subdomain_enum import SubdomainEnum
    monkeypatch.setattr('requests.get', lambda *a, **k: DummyResponse(...))
    se = SubdomainEnum(target="example.com")
    assert "sub.example.com" in se.run()
CI & Workflow
Fork & PR against main.

Ensure ≥80% coverage.

PR triggers GitHub Actions: lint, pytest, mkdocs build.

Merge upon green checks.
