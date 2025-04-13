import subprocess
import os

SURICATA_INTERFACE = "eth0"

def start_suricata():
    cmd = ["sudo", "suricata", "-i", SURICATA_INTERFACE, "-D"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_suricata():
    subprocess.run(["sudo", "pkill", "suricata"])

def is_running():
    result = subprocess.run(["pgrep", "suricata"], stdout=subprocess.DEVNULL)
    return result.returncode == 0
