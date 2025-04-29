import sys
import os
import argparse
import logging
from src.recon import ReconModule
from src.scanner import ScannerModule
from src.brute_force import BruteForceModule
from src.exploits import ExploitModule
from utils.logger import setup_logging
from utils.settings import load_settings

# Set up logging
setup_logging()

# Load configuration settings
config = load_settings()

def run_recon():
    recon = ReconModule(config)
    recon.run()

def run_scanner():
    scanner = ScannerModule(config)
    scanner.run()

def run_brute_force():
    brute_force = BruteForceModule(config)
    brute_force.run()

def run_exploits():
    exploits = ExploitModule(config)
    exploits.run()

def display_banner():
    print("""
    =====================================
    X-Vector Pro - Advanced Pen Testing
    =====================================
    """)

def main():
    # Display the tool banner
    display_banner()

    # Set up argument parser for CLI options
    parser = argparse.ArgumentParser(description="X-Vector Pro - Penetration Testing Tool")
    parser.add_argument('-r', '--recon', action='store_true', help="Run Recon Module")
    parser.add_argument('-s', '--scanner', action='store_true', help="Run Scanner Module")
    parser.add_argument('-b', '--bruteforce', action='store_true', help="Run Brute Force Module")
    parser.add_argument('-e', '--exploits', action='store_true', help="Run Exploits Module")
    parser.add_argument('-v', '--version', action='version', version='X-Vector Pro v1.0', help="Display version information")

    args = parser.parse_args()

    if args.recon:
        run_recon()
    elif args.scanner:
        run_scanner()
    elif args.bruteforce:
        run_brute_force()
    elif args.exploits:
        run_exploits()
    else:
        print("No module selected. Use -h for help.")
        sys.exit(1)

if __name__ == "__main__":
    main()
