import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO)

SURICATA_INTERFACE = os.getenv("SURICATA_INTERFACE", "eth0")

def start_suricata():
    """
    Starts the Suricata IDS on the specified interface.
    """
    try:
        cmd = ["sudo", "suricata", "-i", SURICATA_INTERFACE, "-D"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logging.info("Suricata started successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error starting Suricata: {e}")

def stop_suricata():
    """
    Stops the Suricata IDS.
    """
    try:
        subprocess.run(["sudo", "pkill", "suricata"], check=True)
        logging.info("Suricata stopped successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error stopping Suricata: {e}")

def is_running():
    """
    Checks if Suricata is running.

    Returns:
        bool: True if Suricata is running, False otherwise.
    """
    try:
        result = subprocess.run(["pgrep", "suricata"], stdout=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
