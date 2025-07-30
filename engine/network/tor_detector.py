import logging
import re
import ipaddress
import json
from datetime import datetime
from typing import Dict, Union, List
import argparse
import os

# Setup logger
logger = logging.getLogger("tor_detector")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

# Tor exit node detection - Patterns
TOR_PATTERNS = [
    r"\.onion$",  # .onion TLD
    r"^185\.220\.(100|101|102)\.\d+$",
    r"^154\.(\d+)\.(\d+)\.(\d+)$",
    r"^51\.(\d+)\.(\d+)\.(\d+)$"
]
TOR_REGEX = [re.compile(p) for p in TOR_PATTERNS]

# Subnet blocks
TOR_SUBNET_BLOCKS = [
    "185.220.100.0/22",
    "51.15.0.0/16",
    "154.35.0.0/16"
]

# Confidence map
CONFIDENCE_MAP = {
    "pattern_match_0": 0.98,
    "pattern_match_1": 0.95,
    "pattern_match_2": 0.92,
    "pattern_match_3": 0.90,
    "subnet_match": 0.85
}

def is_ip_in_subnet(ip: str, subnets: List[str]) -> bool:
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        return False
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in ipaddress.ip_network(block) for block in subnets)
    except ValueError:
        return False

def run_detection(target: str) -> Dict[str, Union[str, Dict]]:
    target = target.lower().strip()
    logger.info(f"Running Tor detection for: {target}")
    detected = False
    detection_method = None

    for idx, pattern in enumerate(TOR_REGEX):
        if pattern.search(target):
            detected = True
            detection_method = f"pattern_match_{idx}"
            break

    if not detected and is_ip_in_subnet(target, TOR_SUBNET_BLOCKS):
        detected = True
        detection_method = "subnet_match"

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if detected:
        confidence = CONFIDENCE_MAP.get(detection_method, 0.80)
        logger.warning(f"[!] Tor Detected via {detection_method} (confidence: {confidence})")
        return {
            "status": "stealth",
            "message": "Tor network access detected",
            "details": {
                "target": target,
                "detection_method": detection_method,
                "severity": "medium",
                "timestamp": now,
                "confidence": confidence
            }
        }

    logger.info("[+] No Tor patterns matched.")
    return {
        "status": "clear",
        "message": "No Tor traffic found",
        "details": {
            "target": target,
            "timestamp": now
        }
    }

def save_result(result: Dict, filepath: str = "tor_detection_report.json"):
    with open(filepath, "a") as f:
        json.dump(result, f)
        f.write("\n")
    logger.info(f"[+] Saved result to {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tor Network Detector")
    parser.add_argument("--target", required=True, help="Target IP or domain")
    parser.add_argument("--save", help="File path to save result")
    args = parser.parse_args()

    result = run_detection(args.target)
    print(json.dumps(result, indent=2))

    if args.save:
        save_result(result, args.save)
