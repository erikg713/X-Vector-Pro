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

