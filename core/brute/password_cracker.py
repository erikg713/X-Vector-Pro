import hashlib
import itertools
import time

class PasswordCracker:
    def __init__(self, hash_value, charset="abcdefghijklmnopqrstuvwxyz0123456789", max_length=5):
        self.hash_value = hash_value.lower()
        self.charset = charset
        self.max_length = max_length

    def crack(self):
        start_time = time.time()
        for length in range(1, self.max_length + 1):
            for attempt in itertools.product(self.charset, repeat=length):
                candidate = ''.join(attempt)
                if hashlib.sha256(candidate.encode()).hexdigest() == self.hash_value:
                    elapsed = time.time() - start_time
                    return {"password": candidate, "attempts": length, "time_taken": elapsed}
        return {"error": "Password not found"}

# Example
if __name__ == "__main__":
    hash_to_crack = hashlib.sha256("admin".encode()).hexdigest()
    cracker = PasswordCracker(hash_to_crack)
    result = cracker.crack()
    print(result)
