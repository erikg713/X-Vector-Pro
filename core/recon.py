# core/recon.py

from core import logger, configuration

def passive_recon(target):
    logger.info(f"Starting passive recon on {target}")
    
    # Check stealth mode
    if configuration.get("stealth_mode"):
        logger.info("Stealth mode enabled – minimizing footprint.")

    # Simulated recon logic
    result = f"Passive recon result for {target}: Open WHOIS, DNS, and Shodan results"

    logger.info("Passive recon complete.")
    return result
