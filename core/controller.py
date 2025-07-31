from core.recon import passive_recon
from core.scanner import run_port_scan
from core.brute import brute_force_login, xmlrpc_brute
from core.exploits.exploit_01 import run as run_exploit_01
from core.report import generate_report
from utils.logger import log
from utils import stealth
from core import recon
from core.neural_engine.learning_engine import LearningEngine
from core.recon import ReconEngine
from core.brute import BruteEngine
from core.cve_scanner import CVEScanner
from core.logger import log_event

class XVectorController:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def run_recon(self):
        recon = ReconEngine(self.target)
        recon_results = recon.run_full_recon()
        self.results['recon'] = recon_results
        log_event("controller", {"step": "recon_complete", "results": recon_results})
        return recon_results

    def run_plugin_scan(self):
        # Assuming plugin scan is part of recon results or a separate module
        # For now, dummy plugins detected:
        plugins = {
            "akismet": "4.1",
            "yoast-seo": "15.2"
        }
        self.results['plugins'] = plugins
        log_event("controller", {"step": "plugin_scan_complete", "plugins": plugins})
        return plugins

    def run_brute_force(self):
        brute = BruteEngine(self.target)
        brute.load_wordlist('data/wordlists/passwords.txt')
        brute.start()
        self.results['brute'] = 'completed'
        log_event("controller", {"step": "brute_force_complete"})
        return 'brute force completed'

    def run_cve_check(self):
        plugins = self.results.get('plugins', {})
        cve_scanner = CVEScanner(self.target, plugins)
        cves = cve_scanner.scan()
        self.results['cves'] = cves
        log_event("controller", {"step": "cve_scan_complete", "cves_found": cves})
        return cves

    def run_full_pipeline(self):
        log_event("controller", {"action": "start_full_pipeline", "target": self.target})
        self.run_recon()
        self.run_plugin_scan()
        self.run_brute_force()
        self.run_cve_check()
        log_event("controller", {"action": "pipeline_complete", "results": self.results})
        return self.results


if __name__ == "__main__":
    target = "example.com"
    controller = XVectorController(target)
    final_results = controller.run_full_pipeline()
    print(final_results)

class AutoController:
    def __init__(self):
        self.engine = LearningEngine(mode="deep")  # or "rf"
        self.recon_module = ...
        self.scan_module = ...
        self.brute_module = ...
        self.exploit_module = ...
        self.report_module = ...

    def run_auto(self, target):
        recon_data = self.recon_module.run(target)
        scan_data = self.scan_module.run(target)
        combined_features = self._extract_features(recon_data, scan_data)

        decision = self.engine.select_action(combined_features)
        print(f"[AI Decision] Action: {decision}")

        if decision == "monitor":
            self.report_module.log_passive(target)
        elif decision == "alert":
            self.brute_module.run(target)
        elif decision == "isolate":
            self.exploit_module.run_all(target)

    def _extract_features(self, recon, scan):
        # Normalize and vectorize recon + scan data
        features = [...]  # Convert recon/scan to fixed-length float array
        return features
        
def run_full_auto(target):
    print("[*] Starting Full Auto Recon...")
    recon_report = recon.run_auto_recon(target)
    print(recon_report)
    # Next steps: scanner, brute, exploit, etc.
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
