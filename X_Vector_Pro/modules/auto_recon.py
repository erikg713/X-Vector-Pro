import os
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def parse_xml_summary(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        summary = []

        for host in root.findall("host"):
            ip = host.findtext("address[@addrtype='ipv4']")
            ports = host.find("ports")
            port_summary = []

            if ports:
                for port in ports.findall("port"):
                    port_id = port.get("portid")
                    protocol = port.get("protocol")
                    state = port.findtext("state[@state]")
                    service = port.find("service")
                    service_name = service.get("name") if service is not None else "unknown"
                    port_summary.append(f"{protocol}/{port_id}: {state} ({service_name})")

            summary.append({
                "ip": ip,
                "ports": port_summary
            })
        return summary
    except Exception as e:
        print(f"[!] Failed to parse XML: {e}")
        return []

def save_to_mongodb(scan_data, scan_meta):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["xvector"]
        collection = db["auto_recon"]

        doc = {
            "timestamp": scan_meta["timestamp"],
            "target": scan_meta["target"],
            "raw_output_file": scan_meta["filename"],
            "summary": scan_data
        }

        collection.insert_one(doc)
        print("[+] Saved scan summary to MongoDB.")
    except Exception as e:
        print(f"[!] MongoDB save failed: {e}")

def run_auto_recon(target_ip, output_dir="reports/auto_recon", save_to_db=True):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/vzengines_scan_{timestamp}"

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

    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap scan failed: {e}")

# Example usage
if __name__ == "__main__":
    target = input("Enter target IP or domain: ")
    run_auto_recon(target)
