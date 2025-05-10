import customtkinter as ctk
from core import recon
from core.recon import passive_recon, perform_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login, xmlrpc_brute
from core.exploits.exploit_01 import run as run_exploit_01
from core.report import generate_report
from utils.logger import log
from utils import stealth

# Enable stealth at startup
stealth.enable_stealth()
stealth.start_background_thread()

def run_full_auto(target):
    log("[*] Starting Full Auto Recon...")
    recon_report = recon.run_auto_recon(target)
    print(recon_report)
    return recon_report

def auto_chain_execution(target):
    log("[*] Starting Automated Chain Execution...")
    stealth.apply_stealth_behavior()

    # Queue tasks sequentially (can be adapted for threading)
    stealth.queue_task(lambda: perform_recon(target))
    stealth.queue_task(lambda: run_port_scan(target))
    stealth.queue_task(lambda: brute_force_login(target))
    stealth.queue_task(lambda: run_exploit_01(target))
    stealth.queue_task(generate_report)

def start_brute_force(url, username):
    log("[*] Launching XML-RPC brute force...")
    return xmlrpc_brute(url, username)

def run_automode_chain(target="127.0.0.1"):
    output = []

    log("[*] Starting passive recon...")
    output.append(passive_recon(target))

    log("[*] Running port scan...")
    output.append(run_port_scan(target))

    log("[*] Starting brute force...")
    output.append(brute_force_login(target))

    log("[*] Running default exploit (Exploit 01)...")
    output.append(run_exploit_01(target))

    log("[*] Generating report...")
    output.append(generate_report())

    return "\n\n".join(output)
