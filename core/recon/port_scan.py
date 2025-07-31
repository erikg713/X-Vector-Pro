import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080, 8443]

class PortScanner:
    def __init__(self, target_ip, ports=None, timeout=1):
        self.target_ip = target_ip
        self.timeout = timeout
        self.ports = ports or COMMON_PORTS
        self.open_ports = []

    def scan_port(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                result = sock.connect_ex((self.target_ip, port))
                if result == 0:
                    return port
            except socket.error:
                return None

    def run(self):
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.scan_port, port): port for port in self.ports}
            for future in as_completed(futures):
                port = future.result()
                if port:
                    self.open_ports.append(port)
        return self.open_ports
