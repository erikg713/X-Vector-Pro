import subprocess
from datetime import datetime
import os

CAPTURE_DIR = "logs/pcaps"

def start_capture(interface="eth0", duration=60):
    if not os.path.exists(CAPTURE_DIR):
        os.makedirs(CAPTURE_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(CAPTURE_DIR, f"capture_{timestamp}.pcap")
    
    print(f"[+] Capturing traffic to {filename}...")
    cmd = ["sudo", "tcpdump", "-i", interface, "-w", filename, "-G", str(duration), "-W", "1"]
    subprocess.run(cmd)

    return filename
