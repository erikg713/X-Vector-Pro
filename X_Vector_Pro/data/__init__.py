# X_Vector_Pro/data/__init__.py

"""
Data package for X-Vector Pro.
Contains wordlists, CVE databases, payloads, templates, and cached recon data.
"""

# You can optionally load default paths here if needed
import os

DATA_DIR = os.path.dirname(__file__)

# Example predefined paths
WORDLISTS_DIR = os.path.join(DATA_DIR, 'wordlists')
CVE_DB_PATH = os.path.join(DATA_DIR, 'cve_db.json')
TEMPLATES_DIR = os.path.join(DATA_DIR, 'templates')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')

def list_wordlists():
    """List all wordlists available."""
    if not os.path.exists(WORDLISTS_DIR):
        return []
    return [f for f in os.listdir(WORDLISTS_DIR) if os.path.isfile(os.path.join(WORDLISTS_DIR, f))]

# You could add more utility functions here later
