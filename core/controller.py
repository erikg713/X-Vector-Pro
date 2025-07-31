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
        # Dummy plugins for now
        plugins = {"akismet": "4.1", "yoast-seo": "15.2"}
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
    results = controller.run_full_pipeline()
    print(results)
