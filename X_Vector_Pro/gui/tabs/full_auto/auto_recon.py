import os
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from pymongo import MongoClient
import base64
import json

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "xvector"
COLLECTION_NAME = "auto_recon"
OUTPUT_DIR = "reports/auto_recon"

def base64_encrypt(data):
    return base64.b64encode(json.dumps(data).encode()).decode()

def parse_xml_summary(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        summary = []

        for host in root.findall("host"):
            ip_elem = host.find("address")
            ip = ip_elem.get("addr") if ip_elem is not None else "N/A"
            ports = host.find("ports")
            port_summary = []

            if ports:
                for port in ports.findall("port"):
                    port_id = port.get("portid")
                    protocol = port.get("protocol")
                    state_elem = port.find("state")
                    state = state_elem.get("state") if state_elem is not None else "unknown"
                    service_elem = port.find("service")
                    service_name = service_elem.get("name") if service_elem is not None else "unknown"
                    port_summary.append(f"{protocol}/{port_id}: {state} ({service_name})")

            summary.append({
                "ip": ip,
                "ports": port_summary
            })
        return summary

    except Exception as e:
        print(f"[!] XML parsing failed: {e}")
        return []

def save_to_mongodb(scan_data, scan_meta):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        encrypted_data = base64_encrypt(scan_data)

        doc = {
            "timestamp": scan_meta["timestamp"],
            "target": scan_meta["target"],
            "filename": scan_meta["filename"],
            "summary_encrypted": encrypted_data
        }

        collection.insert_one(doc)
        print("[+] Scan summary saved to MongoDB (encrypted).")
    except Exception as e:
        print(f"[!] MongoDB error: {e}")

def run_auto_recon(target_ip, output_dir=None, save_to_db=True):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target_ip.replace(":", "_").replace("/", "_").replace(" ", "_")

    # Default output folder inside reports
    if not output_dir:
        output_dir = os.path.join("reports", "auto_recon", safe_target)

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"vzengines_scan_{timestamp}")

    command = [
        "nmap", "-T4", "-A", "-p-",
        "--script=default,vuln,auth,discovery,safe",
        "-oA", filename,
        target_ip
    ]

    print(f"[+] Running full auto recon on {target_ip}...")
    try:
        subprocess.run(command, check=True)
        xml_path = f"{filename}.xml"

        print("[+] Parsing scan results...")
        summary = parse_xml_summary(xml_path)
        for host in summary:
            print(f"[*] Host: {host['ip']}")
            for port in host["ports"]:
                print(f"    - {port}")

        if save_to_db:
            scan_meta = {
                "timestamp": timestamp,
                "target": target_ip,
                "filename": filename
            }
            save_to_mongodb(summary, scan_meta)

        return {
            "status": "success",
            "output_dir": output_dir,
            "filename": filename,
            "summary": summary
        }

    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap scan failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
def run_auto_recon(target_ip, stealth=False, save_to_db=True):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/recon_{timestamp}"

    command = [
        "nmap", "-T2" if stealth else "-T4",
        "-A", "-p-", "--script=default,vuln,auth,discovery,safe",
        "-oA", filename,
        target_ip
    ]

    print(f"[+] Starting {'stealth' if stealth else 'full'} recon on {target_ip}...")
    try:
        subprocess.run(command, check=True)
        xml_path = f"{filename}.xml"

        print("[+] Parsing results...")
        summary = parse_xml_summary(xml_path)

        for host in summary:
            print(f"\n[*] Host: {host['ip']}")
            for port in host["ports"]:
                print(f"    - {port}")

        if save_to_db:
            scan_meta = {
                "timestamp": timestamp,
                "target": target_ip,
                "filename": filename
            }
            save_to_mongodb(summary, scan_meta)

    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap execution error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error during scan: {e}")

# CLI Usage
if __name__ == "__main__":
    target = input("Target IP or domain: ")
    stealth = input("Enable stealth mode? (y/n): ").lower() == "y"
    run_auto_recon(target, stealth=stealth)
