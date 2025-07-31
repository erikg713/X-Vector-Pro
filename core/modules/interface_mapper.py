import netifaces

def list_interfaces():
    for iface in netifaces.interfaces():
        print(f"Interface: {iface}")
        addrs = netifaces.ifaddresses(iface)
        for proto, addr_list in addrs.items():
            for addr in addr_list:
                print(f"  {proto}: {addr}")

if __name__ == "__main__":
    list_interfaces()
