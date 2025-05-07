"""Initialization for the gui.tabs package.

Defines shared file paths for logs, sessions, and wordlists.
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HITS_FILE = os.path.join(BASE_DIR, "logs", "hits.txt")
SESSION_FILE = os.path.join(BASE_DIR, "logs", "session.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "xvector_log.txt")
WORDLIST_DIR = os.path.join(BASE_DIR, "wordlists")

# Ensure necessary directories exist
for path in [os.path.join(BASE_DIR, "logs"), WORDLIST_DIR]:
    os.makedirs(path, exist_ok=True)

__all__ = ["HITS_FILE", "SESSION_FILE", "LOG_FILE", "WORDLIST_DIR"]
