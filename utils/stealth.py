import random
import time
import threading
import requests
import logging
import base64
import json
import os
import subprocess
from datetime import datetime
from queue import Queue

def enable_stealth_mode(root, set_status_callback, toast_manager):
    def _stealth():
        set_status_callback("Stealth mode ON")
        toast_manager.show("Stealth mode activated", "info")
        time.sleep(3)
        root.withdraw()  # actually hide the window
        write_encrypted_log("Main window hidden in stealth mode")
    threading.Thread(target=_stealth, daemon=True).start()
    """

    def _stealth():
        set_status_callback("Stealth mode ON")
        toast_manager.show("Stealth mode activated", "info")
        # example: after 3 seconds, hide the window
        time.sleep(3)
        set_status_callback("Stealth: hiding window")
        toast_manager.show("Window hidden (stealth)", "info")
        # note: you could call .withdraw() on the root window here if you pass it in

    threading.Thread(target=_stealth, daemon=True).start()
# --- Configuration ---
PROXY_LIST_PATH = "config/proxies.txt"
ENCRYPTED_LOG_PATH = "logs/stealth.log.enc"
LOG_ENCRYPTION_KEY = "xvector_secret_key"  # Replace with secure env var in production

# --- Background task queue ---
background_tasks = Queue()

# --- Stealth Logger with simple base64 encryption ---
def encrypt_log(data: str, key: str) -> str:
    combined = f"{key}:{data}"
    return base64.b64encode(combined.encode()).decode()

def write_encrypted_log(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    encrypted = encrypt_log(f"{timestamp} {message}", LOG_ENCRYPTION_KEY)
    with open(ENCRYPTED_LOG_PATH, "a") as f:
        f.write(encrypted + "\n")

# --- Random delay injection ---
def random_delay(min_sec=1.0, max_sec=5.0):
    delay = round(random.uniform(min_sec, max_sec), 2)
    write_encrypted_log(f"Sleeping for {delay}s (random delay)")
    time.sleep(delay)

# --- Proxy rotation ---
def load_proxies():
    if not os.path.exists(PROXY_LIST_PATH):
        return []
    with open(PROXY_LIST_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_random_proxy():
    proxies = load_proxies()
    return random.choice(proxies) if proxies else None

def stealth_request(url, **kwargs):
    proxy = get_random_proxy()
    if proxy:
        kwargs['proxies'] = {"http": proxy, "https": proxy}
        write_encrypted_log(f"Using proxy: {proxy}")
    try:
        response = requests.get(url, timeout=10, **kwargs)
        write_encrypted_log(f"GET {url} -> {response.status_code}")
        return response
    except Exception as e:
        write_encrypted_log(f"Request failed: {str(e)}")
        return None

# --- Background task executor ---
def background_worker():
    while True:
        task = background_tasks.get()
        if task is None:
            break
        try:
            task()
        except Exception as e:
            write_encrypted_log(f"Background task error: {str(e)}")
        background_tasks.task_done()

def start_background_thread():
    t = threading.Thread(target=background_worker, daemon=True)
    t.start()
    return t

def queue_task(func):
    background_tasks.put(func)

# --- Tor check / launch ---
def is_tor_running():
    try:
        response = requests.get("http://check.torproject.org", timeout=5)
        return "Congratulations" in response.text
    except:
        return False

def start_tor():
    write_encrypted_log("Attempting to start Tor...")
    try:
        subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        write_encrypted_log(f"Tor start error: {str(e)}")

# --- Stealth mode toggle ---
stealth_mode = {
    "enabled": False,
    "use_tor": False,
    "random_delays": True,
    "proxy_rotation": True
}

def enable_stealth():
    stealth_mode["enabled"] = True
    write_encrypted_log("Stealth mode ENABLED")

def disable_stealth():
    stealth_mode["enabled"] = False
    write_encrypted_log("Stealth mode DISABLED")

def apply_stealth_behavior():
    if stealth_mode["enabled"]:
        if stealth_mode["random_delays"]:
            random_delay()
        if stealth_mode["use_tor"] and not is_tor_running():
            start_tor()

# --- Example usage helper ---
def stealth_execute(func, *args, **kwargs):
    apply_stealth_behavior()
    return func(*args, **kwargs)
