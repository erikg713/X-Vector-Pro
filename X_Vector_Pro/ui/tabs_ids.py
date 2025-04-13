from core.ids.packet_capture import start_capture
import customtkinter as ctk

def build_ids_tab(tab):
    ctk.CTkLabel(tab, text="Suricata & Packet Sniffing", font=("Roboto", 18)).pack(pady=10)

    def capture_now():
        interface = "eth0"
        filename = start_capture(interface=interface, duration=60)
        ctk.CTkLabel(tab, text=f"Capture saved to:\n{filename}", font=("Roboto", 12)).pack()

    ctk.CTkButton(tab, text="Capture Network (60s)", command=capture_now).pack(pady=10)
