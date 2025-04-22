# core/cve_lookup.py

def find_exploits_for_cve(cve_id):
    """
    Simulates searching for exploits by CVE ID.

    Args:
        cve_id (str): CVE identifier

    Returns:
        str: List of matching exploits
    """
    cve_exploit_map = {
        "CVE-2023-12345": ["exploit_01", "exploit_17"],
        "CVE-2022-9999": ["exploit_03"],
        "CVE-2021-40444": ["exploit_09", "exploit_10"]
    }

    exploits = cve_exploit_map.get(cve_id.upper())
    if exploits:
        return f"[+] Found exploits for {cve_id}:\n" + "\n".join(f"- {e}" for e in exploits)
    else:
        return f"[!] No exploits found for {cve_id}."
