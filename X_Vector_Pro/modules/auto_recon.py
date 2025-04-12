import os
import subprocess
from datetime import datetime

def run_auto_recon(target_ip, output_dir="reports/auto_recon"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Timestamped output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/vzengines_scan_{timestamp}"

    # Nmap command
    command = [
        "nmap", "-T4", "-A", "-p-", 
        "--script=default,vuln,auth,discovery,safe",
        "-oA", filename,
        target_ip
    ]

    print(f"[+] Running full auto recon on {target_ip}...")
    try:
        subprocess.run(command, check=True)
        print(f"[+] Scan complete. Output saved to {filename}.[nmap|gnmap|xml]")
    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap scan failed: {e}")

# Example usage
if __name__ == "__main__":
    target = input("Enter target IP or domain: ")
    run_auto_recon(target)
