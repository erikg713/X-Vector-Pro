import os import random

WORDLIST_DIR = os.path.join(os.path.dirname(file), '..', 'wordlists')

class WordlistCombiner: def init(self): self.output_dir = WORDLIST_DIR

def load(self, filename):
    path = os.path.join(WORDLIST_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def combine(self, file1, file2, separator=":", shuffle=True, dedupe=True, output_name="combined_hybrid.txt"):
    list1 = self.load(file1)
    list2 = self.load(file2)

    combined = [f"{a}{separator}{b}" for a in list1 for b in list2]

    if dedupe:
        combined = list(set(combined))

    if shuffle:
        random.shuffle(combined)

    output_path = os.path.join(self.output_dir, output_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(combined))

    return output_path

Example usage:

combiner = WordlistCombiner()

output = combiner.combine('common_usernames.txt', 'simple_passwords.txt')

print(f"Combined wordlist saved to {output}")

