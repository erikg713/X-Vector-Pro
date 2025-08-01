import argparse
import os
import tkinter as tk
from tkinter import ttk
# Your other imports (scanners, exploit modules, etc.)

def parse_args():
    parser = argparse.ArgumentParser(description="X-Vector-Pro CLI Mode")
    parser.add_argument("--auto", action="store_true", help="Run full pipeline")
    parser.add_argument("--target", type=str, help="Target WordPress URL")
    parser.add_argument("--scan-plugins", action="store_true")
    parser.add_argument("--cve-check", action="store_true")
    parser.add_argument("--report-dir", type=str, default="reports/latest")
    return parser.parse_args()

def run_cli_mode(args):
    print(f"[+] Target: {args.target}")
    os.makedirs(args.report_dir, exist_ok=True)

    if args.auto:
        print("[*] Running full pipeline...")
        # call pipeline functions
    if args.scan_plugins:
        print("[*] Scanning plugins...")
        # call plugin scanner
    if args.cve_check:
        print("[*] Checking for CVEs...")
        # call CVE checker

    print(f"[+] Report saved to: {args.report_dir}")

def launch_gui():
    root = tk.Tk()
    root.title("X-Vector-Pro GUI")
    root.geometry("1024x720")
    # GUI init and event bindings here...
    root.mainloop()

if __name__ == "__main__":
    args = parse_args()
    if args.target:
        run_cli_mode(args)
    else:
        launch_gui()
