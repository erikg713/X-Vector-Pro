# X_Vector_Pro/engine/brute_engine.py

"""
Modular Brute-Force Engine for X-Vector Pro

Handles brute-force attacks against detected login endpoints using selected wordlists and plugins.
Supports stealth settings, progress updates, and service-specific modules.
"""

import time
from utils.logger import log_to_central
from utils.stealth import stealth_delay
from core.brute_modules.http_basic import brute_http_basic
from core.brute_modules.wordpress import brute_wordpress
from core.brute_modules.ftp import brute_ftp
from core.brute_modules.ssh import brute_ssh

# Map of supported brute modules
BRUTE_PLUGINS = {
    "http-basic": brute_http_basic,
    "wordpress": brute_wordpress,
    "ftp": brute_ftp,
    "ssh": brute_ssh
}


def run_brute_force(target, services, config, update_callback=None):
    """
    Run brute-force modules against detected services or login pages.
    
    :param target: str - Target IP or domain
    :param services: list - List of service dicts with "type", "port", "url" keys
    :param config: dict - Settings (wordlists, proxy, delays, stealth)
    :param update_callback: callable - Function for UI status updates
    :return: list of successful brute results
    """

    results = []

    def update_ui(msg):
        log_to_central(msg)
        if update_callback:
            update_callback(msg)

    update_ui(f"[BRUTE] Starting brute-force phase on {target}")

    for service in services:
        service_type = service.get("type")
        port = service.get("port")
        url = service.get("url", "")

        update_ui(f"[*] Targeting {service_type.upper()} on port {port}")

        brute_func = BRUTE_PLUGINS.get(service_type)

        if not brute_func:
            update_ui(f"[-] No brute module for service type: {service_type}")
            continue

        try:
            success = brute_func(target=target, port=port, url=url, config=config)
            if success:
                results.append({"service": service_type, "port": port, "creds": success})
                update_ui(f"[+] Success: {success}")
            else:
                update_ui(f"[-] {service_type} brute failed or no valid credentials found.")

        except Exception as e:
            update_ui(f"[ERROR] {service_type} brute module crashed: {e}")

        stealth_delay(config)  # Apply delay if stealth is enabled

    update_ui(f"[BRUTE] Completed brute-force phase with {len(results)} successes.")
    return results
