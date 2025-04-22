# core/recon.py
def passive_recon(target):
    return f"Passive recon on {target} complete. (Fake data)"

# core/scanner.py
def run_port_scan(target):
    return f"Scan on {target}: Port 80 open (Fake result)"

# core/brute.py
def brute_force_login(target):
    return f"Brute force on {target}: No valid credentials found (Fake)"

# core/exploit_01.py
def run(target):
    return f"Exploit_01 run on {target} — simulated success."

# core/report.py
def generate_report():
    return "HTML report generated successfully. (Simulated)"

import os
import subprocess
from datetime import datetime
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from utils.logger import log
from core.recon.recon_engine import ReconEngine
def run_auto_recon(target_ip, output_dir="reports/auto_recon"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/scan_{timestamp}"

    command = [
        "nmap", "-T4", "-A", "-p-",
        "--script=default,vuln,auth,discovery,safe",
        "-oA", filename,
        target_ip
    ]

    log(f"[+] Starting auto recon on {target_ip}")
    try:
        subprocess.run(command, check=True)
        xml_path = f"{filename}.xml"
        summary = parse_xml_summary(xml_path)
        save_to_mongo(summary, target_ip, timestamp, filename)
        return summary
    except subprocess.CalledProcessError as e:
        log(f"[!] Nmap failed: {e}")
        return []

def parse_xml_summary(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        summary = []

        for host in root.findall("host"):
            ip_elem = host.find("address")
            ip = ip_elem.get("addr") if ip_elem is not None else "unknown"
            ports = host.find("ports")
            port_summary = []

            if ports:
                for port in ports.findall("port"):
                    port_id = port.get("portid")
                    proto = port.get("protocol")
                    state = port.find("state").get("state")
                    service = port.find("service")
                    svc_name = service.get("name") if service is not None else "unknown"
                    port_summary.append(f"{proto}/{port_id}: {state} ({svc_name})")

            summary.append({"ip": ip, "ports": port_summary})
        return summary
    except Exception as e:
        log(f"[!] XML parse error: {e}")
        return []

def save_to_mongo(summary, target, timestamp, filename):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["xvector"]
        col = db["auto_recon"]
        doc = {
            "timestamp": timestamp,
            "target": target,
            "output_file": filename,
            "summary": summary
        }
        col.insert_one(doc)
        log(f"[+] Saved auto recon to MongoDB for {target}")
    except Exception as e:
        log(f"[!] MongoDB error: {e}")
import requests
import socket
from utils.logger import log

def basic_recon(target_url):
    log("[*] Starting recon...")

    try:
        ip = socket.gethostbyname(target_url.replace("http://", "").replace("https://", "").split("/")[0])
        headers = requests.get(target_url).headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
    except Exception as e:
        log(f"[!] Recon failed: {e}")
        return

    log(f"[+] IP Address: {ip}")
    log(f"[+] Server: {server}")
    log(f"[+] X-Powered-By: {powered_by}")
