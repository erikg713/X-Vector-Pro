# Brute force module initializer


import socket
from core.logger import log_event

log_event("scan", {"target": "example.com", "status": "open ports found"}, level="info", write_structured_file=True)
from .ftp_brute import ftp_brute_force
from .http_login_brute import http_login_brute
from utils.logger import save_hit, log_event
available_modules = {
    "FTP": {
        "func": ftp_brute_force,
        "default_port": 21,
        "wordlist": "ftp_default_creds.txt"
    },
    "HTTP Login": {
        "func": http_login_brute_force,
        "default_port": 80,
        "wordlist": "http_default_creds.txt"
    },
    # Extend with more protocols/modules
}

port_service_map = {
    21: "FTP",
    80: "HTTP Login",
    443: "HTTPS Login"
}

def detect_service(port):
    return port_service_map.get(port, None)

def run_brute_force(module_name=None, target="", port=None, wordlist_file=None,
                    stealth_mode=False, timeout=5, logger=print):
    logger(f"[*] Starting brute-force on {target}:{port or 'default'}")

    if not module_name and port:
        module_name = detect_service(port)
        if module_name:
            logger(f"[~] Auto-detected module: {module_name}")
        else:
            logger("[!] Unknown service for port; can't detect module.")
            return {"status": "failed", "reason": "unknown_service"}

    if module_name not in available_modules:
        logger(f"[!] Unsupported brute-force module: {module_name}")
        return {"status": "failed", "reason": "unsupported_module"}

    module = available_modules[module_name]
    port = port or module["default_port"]
    wordlist_file = wordlist_file or module["wordlist"]

    try:
        result = module["func"](
            target=target,
            port=port,
            wordlist_file=wordlist_file,
            stealth_mode=stealth_mode,
            timeout=timeout,
            logger=logger
        )
        return {
            "status": result.get("status", "failed"),
            "module": module_name,
            "target": target,
            "port": port,
            "result": result
        }
    except Exception as e:
        logger(f"[!] Error during brute-force: {e}")
        return {"status": "failed", "error": str(e)}
