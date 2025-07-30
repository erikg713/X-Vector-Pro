import argparse
import sys
import json

from core.brute_force_wallet import BruteEngine
from engine.recon import ReconEngine
from engine.scanner import PluginScanner
from engine.cve_checker import CVEChecker
from gui.app import XVectorProApp

def run_full_pipeline(target, report_dir=None):
    print(f"[+] Starting full pipeline against {target}")
    recon = ReconEngine(target)
    scan = PluginScanner(target)
    brute = BruteEngine(target)
    cve = CVEChecker()

    recon_results = recon.run()
    scan_results = scan.run()
    brute.load_wordlist("data/wordlists/passwords.txt")
    brute_results = brute.start()
    cve_results = cve.check_plugins(scan_results)

    report = {
        "target": target,
        "recon": recon_results,
        "scan": scan_results,
        "brute_force": brute_results,
        "cve": cve_results,
    }

    if report_dir:
        report_file = f"{report_dir}/report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[+] Report saved to {report_file}")

    return report

def main():
    parser = argparse.ArgumentParser(description="X-Vector Pro WordPress Attack Suite")
    parser.add_argument("--auto", action="store_true", help="Run full pipeline (Recon → Scan → Plugins → Exploits)")
    parser.add_argument("--target", help="Target WordPress URL (e.g. https://site.local)")
    parser.add_argument("--scan-plugins", action="store_true", help="Enumerate installed plugins and versions")
    parser.add_argument("--cve-check", action="store_true", help="Detect local CVEs from data/cve_db.json")
    parser.add_argument("--report-dir", help="Directory to save logs & HTML reports")
    parser.add_argument("--gui", action="store_true", help="Launch GUI application")
    args = parser.parse_args()

    if args.gui:
        app = XVectorProApp()
        app.run()
        sys.exit(0)

    if not args.target:
        print("[-] Error: --target argument is required for CLI operations.")
        sys.exit(1)

    if args.auto:
        run_full_pipeline(args.target, args.report_dir)
    else:
        if args.scan_plugins:
            scanner = PluginScanner(args.target)
            plugins = scanner.run()
            print(f"[+] Plugins found: {plugins}")

        if args.cve_check:
            cve = CVEChecker()
            results = cve.check_plugins([])  # Ideally pass scanned plugins
            print(f"[+] CVE Results: {results}")

if __name__ == "__main__":
    main()
