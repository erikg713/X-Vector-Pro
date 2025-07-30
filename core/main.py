#!/usr/bin/env python3
import argparse
import sys
import json

# CLI Engines
from core.brute_force_wallet import BruteEngine
from engine.recon       import ReconEngine
from engine.scanner     import PluginScanner
from engine.cve_checker import CVEChecker

# GUI launcher
from gui.app import XVectorProApp


def run_full_pipeline(target, report_dir=None):
    """
    Runs Recon → Scan → Brute → CVE checks,
    then dumps a JSON report if requested.
    """
    print(f"[+] Starting full pipeline against {target}")

    recon = ReconEngine(target)
    scan  = PluginScanner(target)
    brute = BruteEngine(target)
    cve   = CVEChecker()

    recon_results = recon.run()
    scan_results  = scan.run()
    brute.load_wordlist("data/wordlists/passwords.txt")
    brute_results = brute.start()
    cve_results   = cve.check_plugins(scan_results)

    report = {
        "target":      target,
        "recon":       recon_results,
        "scan":        scan_results,
        "brute_force": brute_results,
        "cve":         cve_results,
    }

    if report_dir:
        filepath = f"{report_dir}/report.json"
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[+] Report saved to {filepath}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="X-Vector Pro WordPress Attack Suite"
    )
    parser.add_argument("--gui",         action="store_true", help="Launch the GUI")
    parser.add_argument("--auto",        action="store_true",
                        help="Run full pipeline (Recon → Scan → Brute → CVE)")
    parser.add_argument("--scan-plugins",action="store_true",
                        help="Enumerate installed plugins and versions")
    parser.add_argument("--cve-check",   action="store_true",
                        help="Detect CVEs from local database")
    parser.add_argument("--report-dir",  help="Directory to save JSON report")
    parser.add_argument("--target",      help="Target WordPress URL")

    args = parser.parse_args()

    # GUI mode
    if args.gui:
        sys.exit(XVectorProApp().run())

    # CLI requires --target
    if not args.target:
        parser.error("the following argument is required: --target")

    # Auto pipeline
    if args.auto:
        run_full_pipeline(args.target, args.report_dir)
        return

    # Individual operations
    if args.scan_plugins:
        scanner = PluginScanner(args.target)
        plugins = scanner.run()
        print(f"[+] Plugins found: {plugins}")

    if args.cve_check:
        cve = CVEChecker()
        results = cve.check_plugins([])  # ideally pass actual plugins
        print(f"[+] CVE Results: {results}")


if __name__ == "__main__":
    main()

