# core/controller.py
from core.recon import passive_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login
from core.exploit_01 import run as run_exploit_01
from core.report import generate_report
from core.auto_mode.sequencer import run_sequence
from core.auto_mode import run_sequence
from core.brute import xmlrpc_brute
from utils.logger import log

def start_brute_force(url, username):
    log("[*] Launching XML-RPC brute force...")
    xmlrpc_brute(url, username)

def run_automode_chain(target="127.0.0.1"):
    return run_sequence(target)
def run_automode_chain(target="127.0.0.1"):
    output = []

    output.append("[*] Starting passive recon...")
    recon_result = passive_recon(target)
    output.append(recon_result)

    output.append("[*] Running port scan...")
    scan_result = run_port_scan(target)
    output.append(scan_result)

    output.append("[*] Starting brute force...")
    brute_result = brute_force_login(target)
    output.append(brute_result)

    output.append("[*] Running default exploit...")
    exploit_result = run_exploit_01(target)
    output.append(exploit_result)

    output.append("[*] Generating report...")
    report = generate_report()
    output.append(report)

    return "\n\n".join(output)
from core.brute import xmlrpc_brute
from utils.logger import log

def start_brute_force(url, username):
    log("[*] Launching XML-RPC brute force...")
    xmlrpc_brute(url, username)
