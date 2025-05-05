import os
import requests
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

# Constants
CONFIG_PATH = "gui/crawl/admin.ini"  # Relative path to the ini file
THREADS = 10  # Number of concurrent requests

def load_admin_paths(config_path):
    """
    Load admin panel paths from the admin.ini file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    paths = []
    with open(config_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Skip comments and empty lines
                paths.append(line)
    return paths

def check_admin_path(base_url, path):
    """
    Check if an admin path exists on the target website.
    """
    url = urljoin(base_url, path)
    try:
        response = requests.head(url, timeout=5)  # Using HEAD for efficiency
        if response.status_code == 200:
            print(f"[FOUND] {url}")
            return url
        else:
            print(f"[NOT FOUND] {url} - Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[ERROR] {url} - {e}")
    return None

def scan_admin_paths(base_url, paths):
    """
    Scan the target website for admin paths.
    """
    found_paths = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(lambda path: check_admin_path(base_url, path), paths)
        found_paths.extend(filter(None, results))
    return found_paths

def main():
    """
    Main function to load paths and scan the target website.
    """
    target_url = input("Enter target URL (e.g., https://example.com): ").strip()
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("[ERROR] Invalid URL. Make sure it starts with http:// or https://")
        return

    try:
        print("[INFO] Loading admin paths...")
        paths = load_admin_paths(CONFIG_PATH)
        print(f"[INFO] Loaded {len(paths)} paths")

        print("[INFO] Scanning for admin panels...")
        found_paths = scan_admin_paths(target_url, paths)

        if found_paths:
            print("\n[RESULTS] Admin Panels Found:")
            for path in found_paths:
                print(f"- {path}")
        else:
            print("\n[RESULTS] No admin panels found.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
