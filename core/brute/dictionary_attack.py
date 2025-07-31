class DictionaryAttack:
    def __init__(self, hash_value, wordlist_path):
        import hashlib
        self.hash_value = hash_value.lower()
        self.wordlist_path = wordlist_path
        self.hashlib = hashlib

    def run(self):
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if self.hashlib.sha256(word.encode()).hexdigest() == self.hash_value:
                        return {"found": True, "password": word}
            return {"found": False}
        except Exception as e:
            return {"error": str(e)}

# Example
if __name__ == "__main__":
    hash_to_crack = "5e884898da28047151d0e56f8dc6292773603d0d6aabbddbbbfbbe20bbf5d8e3"  # 'password'
    da = DictionaryAttack(hash_to_crack, "wordlists/common.txt")
    print(da.run())
