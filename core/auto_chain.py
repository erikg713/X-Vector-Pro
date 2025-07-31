from utils import stealth
from core.recon import perform_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login
from core.exploits.exploit_01 import run as run_exploit_01
from core.report import generate_report
from utils.logger import log

def run_automode_chain(target):
    output = []

    log("[*] Starting passive recon...")
    recon_result = perform_recon(target)
    output.append(recon_result)

    log("[*] Running port scan...")
    scan_result = run_port_scan(target)
    output.append(scan_result)

    log("[*] Starting brute force...")
    brute_result = brute_force_login(target)
    output.append(brute_result)

    log("[*] Running default exploit (Exploit 01)...")
    exploit_result = run_exploit_01(target)
    output.append(exploit_result)

    log("[*] Generating report...")
    report = generate_report()
    output.append(report)

    return "\n\n".join(output)

def start_stealth_mode():
    stealth.enable_stealth()
    stealth.start_background_thread()
    stealth.apply_stealth_behavior()
