import os import random

WORDLIST_DIR = os.path.join(os.path.dirname(file), '..', 'wordlists')

class WordlistManager: def init(self): self.cache = {}

def list_available(self):
    """Return a list of available wordlist files."""
    return [f for f in os.listdir(WORDLIST_DIR) if f.endswith('.txt')]

def load(self, filename, shuffle=False):
    """Load and return a list of words from a wordlist."""
    path = os.path.join(WORDLIST_DIR, filename)
    if path in self.cache:
        words = self.cache[path]
    else:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            self.cache[path] = words
        except FileNotFoundError:
            return []

    if shuffle:
        words = words.copy()
        random.shuffle(words)
    return words

def get_random_wordlist(self):
    """Return a random wordlist file name from available ones."""
    available = self.list_available()
    return random.choice(available) if available else None

def load_random(self):
    """Load a random wordlist (for stealth mode)."""
    filename = self.get_random_wordlist()
    if filename:
        return self.load(filename, shuffle=True)
    return []

Singleton instance for global use

wordlist_manager = WordlistManager()

