from core.ids.packet_capture import start_capture
import customtkinter as ctk

def build_ids_tab(tab):
    ctk.CTkLabel(tab, text="Suricata & Packet Sniffing", font=("Roboto", 18)).pack(pady=10)

    def capture_now():
        interface = "eth0"
        filename = start_capture(interface=interface, duration=60)
        ctk.CTkLabel(tab, text=f"Capture saved to:\n{filename}", font=("Roboto", 12)).pack()

    ctk.CTkButton(tab, text="Capture Network (60s)", command=capture_now).pack(pady=10)
from core.ids.auto_analyzer import check_for_threats

def show_alerts():
    alerts = check_for_threats()
    if not alerts:
        ctk.CTkLabel(tab, text="No threats found.", font=("Roboto", 12)).pack()
    for alert in alerts:
        ctk.CTkLabel(tab, text=f"{alert['timestamp']} - {alert['alert']}", font=("Roboto", 10)).pack()

ctk.CTkButton(tab, text="Check Suricata Alerts", command=show_alerts).pack(pady=5)
