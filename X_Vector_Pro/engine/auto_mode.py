# X_Vector_Pro/engine/auto_mode.py

"""
Auto Mode Controller for X-Vector Pro

Executes full scan chain: Recon → Port Scan → Brute Force → Exploits → Report
Designed for silent, stealth-first, fully automated operations.
"""

import time
from core.recon import run_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login
from core.exploits import run_all_exploits
from core.report import generate_full_report
from utils.logger import log_to_central
from utils.stealth import stealth_delay

def run_auto_mode(target, config, update_callback=None):
    """
    Executes full automated chain on the target with optional live GUI status updates.
    :param target: str, IP or domain to scan.
    :param config: dict, current settings (delay, stealth, wordlists, etc.)
    :param update_callback: function to send status updates to UI.
    """

    def update_ui(message):
        log_to_central(message)
        if update_callback:
            update_callback(message)

    start_time = time.time()
    update_ui(f"[AUTO] Starting full chain on {target}...")

    try:
        # 1. Recon
        update_ui("[*] Recon phase started.")
        recon_data = run_recon(target, config)
        stealth_delay(config)
        update_ui(f"[+] Recon completed. Found: {recon_data}")

        # 2. Port Scan
        update_ui("[*] Running port scan...")
        open_ports = run_port_scan(target, top_n=30, timeout=0.5)
        stealth_delay(config)
        update_ui(f"[+] Port scan complete. Open ports: {open_ports}")

        # 3. Brute Force (only if login pages detected)
        if recon_data.get("login_pages"):
            update_ui("[*] Launching brute-force attacks...")
            brute_results = brute_force_login(target, config, recon_data.get("login_pages"))
            update_ui(f"[+] Brute-force results: {brute_results}")
        else:
            update_ui("[-] No login pages found. Skipping brute-force step.")

        # 4. Exploits
        update_ui("[*] Executing exploits...")
        exploit_results = run_all_exploits(target, config, open_ports)
        update_ui(f"[+] Exploit results: {exploit_results}")

        # 5. Reporting
        update_ui("[*] Generating final report...")
        report_path = generate_full_report(target, recon_data, open_ports, brute_results, exploit_results)
        update_ui(f"[+] Report saved to: {report_path}")

    except Exception as e:
        update_ui(f"[ERROR] Auto mode failed: {e}")

    total_time = time.time() - start_time
    update_ui(f"[AUTO] Full scan completed in {total_time:.2f}s.")
