from core.ids.log_parser import parse_fast_log
from datetime import datetime

def check_for_threats():
    fast_entries = parse_fast_log()
    threat_list = []
    for entry in fast_entries:
        if "ET MALWARE" in entry or "ET TROJAN" in entry:
            threat_list.append({
                "timestamp": datetime.now().isoformat(),
                "alert": entry
            })
    return threat_list
