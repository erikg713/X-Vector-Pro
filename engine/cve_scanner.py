# X_Vector_Pro/engine/cve_scanner.py

"""
CVE Scanner Engine for X-Vector Pro

Matches discovered services, versions, or banners to known CVEs using a local database.
Supports stealth delay, GUI updates, and full result export.
"""

import json
import re
from utils.logger import log_to_central
from utils.stealth import stealth_delay

CVE_DB_PATH = "cve_db.json"


def load_cve_database():
    try:
        with open(CVE_DB_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        log_to_central(f"[ERROR] Failed to load CVE database: {e}")
        return {}


def match_cves(service_data, cve_db, config, update_callback=None):
    """
    Match scanned services against CVE database.

    :param service_data: list of dicts with 'service', 'version', 'banner'
    :param cve_db: dict - Loaded CVE database
    :param config: dict - Settings (stealth, delay, etc.)
    :param update_callback: callable - UI notifier
    :return: list of dicts with matched CVEs
    """
    results = []

    def update_ui(msg):
        log_to_central(msg)
        if update_callback:
            update_callback(msg)

    update_ui("[CVE] Starting CVE scan...")

    for item in service_data:
        service = item.get("service", "").lower()
        version = item.get("version", "").lower()
        banner = item.get("banner", "").lower()

        cves_found = []

        # Match against CVE DB entries
        for cve_id, entry in cve_db.items():
            affected_service = entry.get("service", "").lower()
            version_pattern = entry.get("version_regex", "")
            keyword_match = entry.get("keyword", "").lower()

            if affected_service in service:
                if version_pattern and re.search(version_pattern, version):
                    cves_found.append({**entry, "cve": cve_id})
                elif keyword_match and keyword_match in banner:
                    cves_found.append({**entry, "cve": cve_id})

        if cves_found:
            update_ui(f"[+] Matched {len(cves_found)} CVE(s) for {service} {version}")
            results.append({
                "service": service,
                "version": version,
                "matches": cves_found
            })
        else:
            update_ui(f"[-] No CVEs found for {service} {version}")

        stealth_delay(config)

    update_ui(f"[CVE] CVE scanning complete. Total vulnerable services: {len(results)}")
    return results
