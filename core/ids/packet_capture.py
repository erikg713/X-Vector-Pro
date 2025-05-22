import subprocess
from datetime import datetime
import os
import subprocess
from datetime import datetime
import os

CAPTURE_DIR = "logs/pcaps"

def start_capture(interface="eth0", duration=60):
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(CAPTURE_DIR, f"capture_{timestamp}.pcap")
    print(f"[+] Capturing traffic to {filename}...")

    cmd = [
        "sudo", "tcpdump",
        "-i", interface,
        "-w", filename,
        "-G", str(duration),
        "-W", "1"
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] tcpdump failed: {e.stderr}")
        return None
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return None

    return filename
    
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
