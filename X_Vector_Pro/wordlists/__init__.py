import os

# Base directory for wordlists
WORDLISTS_DIR = os.path.dirname(__file__)

# Supported extensions
ALLOWED_EXTENSIONS = {'.txt', '.lst', '.wl'}

# Cache of discovered wordlists
available_wordlists = {}

# Scan and cache wordlists
def scan_wordlists():
    global available_wordlists
    available_wordlists.clear()
    for root, _, files in os.walk(WORDLISTS_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                category = os.path.relpath(root, WORDLISTS_DIR)
                path = os.path.join(root, file)
                if category not in available_wordlists:
                    available_wordlists[category] = []
                available_wordlists[category].append(path)

# Load a wordlist by category and name
def load_wordlist(category, filename):
    scan_wordlists()
    paths = available_wordlists.get(category, [])
    for path in paths:
        if path.endswith(filename):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
    raise FileNotFoundError(f"Wordlist '{filename}' not found in category '{category}'")

# Return available categories and files
def list_wordlists():
    scan_wordlists()
    return available_wordlists

# Initial scan on import
scan_wordlists()
