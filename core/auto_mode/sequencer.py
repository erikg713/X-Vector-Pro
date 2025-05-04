from core.recon import passive_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login
from core.exploit_01 import run as run_exploit_01
from core.report import generate_report

def run_sequence(target="127.0.0.1"):
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
