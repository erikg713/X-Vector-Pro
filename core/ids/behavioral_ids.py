import scapy.all as scapy
from core.ids.behavioral_ids import BehavioralIDS

ids = BehavioralIDS()

def extract_features(packet):
    try:
        proto = packet.proto if hasattr(packet, 'proto') else 0
        length = len(packet)
        entropy = sum([ord(c) for c in str(packet)]) % 256
        return [proto, length, entropy]
    except:
        return [0, 0, 0]

def start_sniff(interface="eth0"):
    print(f"[Sniffer] Listening on {interface}...")
    scapy.sniff(iface=interface, prn=process_packet, store=False)

def process_packet(packet):
    features = extract_features(packet)
    ids.analyze(features)
