import json
import os

def find_exploits_for_cve(cve_id, db_path="cve_db.json"):
    """
    Searches for known exploits by CVE ID.

    First attempts to load from a local JSON database file.
    Falls back to a built-in mock dictionary if the file doesn't exist or fails to load.

    Args:
        cve_id (str): CVE identifier
        db_path (str): Path to the CVE exploit database file

    Returns:
        str: Human-readable list of found exploits or a message if none found
    """
    cve_id = cve_id.upper()

    # Try loading from JSON file if it exists
    if os.path.isfile(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                cve_map = json.load(f)
                cve_map = {k.upper(): v for k, v in cve_map.items()}  # normalize keys
            exploits = cve_map.get(cve_id)
            if exploits:
                return f"[+] Found exploits for {cve_id} (from database):\n" + "\n".join(f"- {e}" for e in exploits)
            else:
                return f"[!] No exploits found for {cve_id} in database."
        except Exception as e:
            return f"[!] Failed to load exploit database: {e}"

    # Fallback mock DB
    print("[*] Using fallback exploit data.")
    fallback_data = {
        "CVE-2023-12345": ["ExploitDB ID: 12345 - Remote buffer overflow in FooServer"],
        "CVE-2022-5678": ["ExploitDB ID: 56789 - SQL injection in BarCMS"],
        "CVE-2021-40444": ["ExploitDB ID: 77777 - MS Office ActiveX RCE"]
    }

    exploits = fallback_data.get(cve_id)
    if exploits:
        return f"[+] Found exploits for {cve_id} (fallback):\n" + "\n".join(f"- {e}" for e in exploits)
    else:
        return f"[!] No exploits found for {cve_id}."

# Optional: Run from command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cve_lookup.py <CVE-ID>")
    else:
        result = find_exploits_for_cve(sys.argv[1])
        print(result)
