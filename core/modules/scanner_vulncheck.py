from python_nmap import NmapProcess, NmapParser

def vuln_check(ip):
    nmproc = NmapProcess(ip, options="-sV --script vuln")
    rc = nmproc.run()
    if rc != 0:
        raise Exception("Nmap scan failed: " + nmproc.stderr)
    parsed = NmapParser.parse(nmproc.stdout)
    for host in parsed.hosts:
        print(f"[{host.address}]")
        for svc in host.services:
            print(f"  {svc.port}/{svc.protocol} - {svc.service} - {svc.state}")
            for script in svc.scripts_results:
                print(f"    Script: {script['id']} - Output: {script['output']}")

if __name__ == "__main__":
    ip = input("Enter IP: ")
    vuln_check(ip)
