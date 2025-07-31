import nmap

def scan_ports(target):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=target, arguments='-sS -p 1-65535')
    results = {}
    for host in scanner.all_hosts():
        results[host] = scanner[host].all_protocols()
    return results

if __name__ == "__main__":
    from rich import print
    target_ip = input("Enter IP to scan: ")
    output = scan_ports(target_ip)
    print(output)
