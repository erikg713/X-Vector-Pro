import json

FAST_LOG_PATH = "/var/log/suricata/fast.log"
EVE_LOG_PATH = "/var/log/suricata/eve.json"

def parse_fast_log():
    events = []
    with open(FAST_LOG_PATH, "r") as f:
        for line in f:
            events.append(line.strip())
    return events

def parse_eve_alerts():
    alerts = []
    with open(EVE_LOG_PATH, "r") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("event_type") == "alert":
                alerts.append(entry)
    return alerts
