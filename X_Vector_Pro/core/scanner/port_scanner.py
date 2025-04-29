import socket
import threading

class PortScanner:
    def __init__(self, target_ip, port_range, logger, timeout=2):
        """
        Initialize the PortScanner object.
        
        Args:
            target_ip (str): The IP address of the target system.
            port_range (tuple): A tuple of the form (start_port, end_port).
            logger (function): A logging function to log messages.
            timeout (int): Timeout value for socket connection attempts. Default is 2 seconds.
        """
        self.target_ip = target_ip
        self.port_range = port_range
        self.logger = logger
        self.timeout = timeout
        self.open_ports = []

    def scan_ports(self):
        """
        Scan the specified range of ports on the target system.
        """
        self.logger(f"[*] Scanning ports {self.port_range[0]}-{self.port_range[1]} on {self.target_ip}...")
        
        threads = []
        for port in range(self.port_range[0], self.port_range[1] + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        # Join threads to wait for all of them to finish
        for thread in threads:
            thread.join()

        if self.open_ports:
            self.logger(f"[+] Found open ports: {', '.join(map(str, self.open_ports))}")
        else:
            self.logger("[*] No open ports found.")

    def scan_port(self, port):
        """
        Scan a single port on the target system.
        
        Args:
            port (int): The port to be scanned.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target_ip, port))
                
                if result == 0:  # Port is open
                    self.open_ports.append(port)
                    self.logger(f"[+] Open port found: {port}")
        except socket.error as e:
            self.logger(f"[-] Error scanning port {port}: {e}")

# Example logger function
def simple_logger(message):
    print(message)

# Example usage
if __name__ == "__main__":
    target_ip = "192.168.1.1"
    port_range = (1, 1024)  # Scanning ports from 1 to 1024
    port_scanner = PortScanner(target_ip, port_range, simple_logger)
    
    # Start scanning ports
    port_scanner.scan_ports()
