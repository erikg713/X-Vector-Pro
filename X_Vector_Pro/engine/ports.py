# engine/ports.py
import socket, tldextract

class PortScanner:
    def __init__(self, url_or_ip, logger):
        self.target = url_or_ip
        self.log = logger
        self.ports = [21, 22, 80, 443, 3306]

    def run(self, findings=None):
        try:
            ip = self.target
            if not ip.replace('.', '').isdigit():
                ip = socket.gethostbyname(tldextract.extract(ip).registered_domain)

            self.log("[*] Running Port Scan...")
            for port in self.ports:
                try:
                    with socket.socket() as s:
                        s.settimeout(0.3)
                        if s.connect_ex((ip, port)) == 0:
                            if findings is not None:
                                findings["open_ports"].append(port)
                            self.log(f"    [+] Port {port} open")
                except:
                    continue
        except Exception as e:
            self.log(f"[!] Port scan failed: {e}")
