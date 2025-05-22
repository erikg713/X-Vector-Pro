# core/ids/portscan_ids.py

import socket

def run_detection(target):
    common_ports = [21, 22, 23, 80, 443, 3389]
    open_ports = []

    for port in common_ports:
        try:
            with socket.create_connection((target, port), timeout=1):
                open_ports.append(port)
        except:
            continue

    if open_ports:
        return {
            "status": "suspicious",
            "message": f"Open common ports detected: {open_ports}"
        }
    else:
        return {
            "status": "clear",
            "message": "No common ports open."
        }
