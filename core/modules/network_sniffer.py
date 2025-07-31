from scapy.all import sniff

def packet_callback(packet):
    print(f"[+] Packet: {packet.summary()}")

def start_sniff(interface="eth0"):
    sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    iface = input("Enter interface: ")
    start_sniff(iface)
