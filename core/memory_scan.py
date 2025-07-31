import psutil
import re

def search_memory(pattern: str) -> list:
    results = []
    regex = re.compile(pattern.encode())
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            with open(f"/proc/{proc.pid}/mem", 'rb', 0) as mem:
                chunk = mem.read(1024*1024)
                if regex.search(chunk):
                    results.append({"pid": proc.pid, "name": proc.name()})
        except Exception:
            continue
    return results
