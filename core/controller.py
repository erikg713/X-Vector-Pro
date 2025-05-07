from core.recon import passive_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login, xmlrpc_brute
from core.exploits.exploit_01 import run as run_exploit_01
from core.report import generate_report
from utils.logger import log
from utils import stealth

# Enable stealth at startup
stealth.enable_stealth()
stealth.start_background_thread()

def auto_chain_execution(target):
    stealth.apply_stealth_behavior()

    # Step 1: Recon
    from core.recon import perform_recon
    stealth.queue_task(lambda: perform_recon(target))

    # Step 2: Scan, Brute, Exploit...
    # queue other steps similarly
def start_brute_force(url, username):
    log("[*] Launching XML-RPC brute force...")
    return xmlrpc_brute(url, username)

def run_automode_chain(target="127.0.0.1"):
    output = []

    log("[*] Starting passive recon...")
    recon_result = passive_recon(target)
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
