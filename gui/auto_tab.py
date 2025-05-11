import customtkinter as ctk

def build_tab(parent):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text="Auto Mode (Placeholder)", font=("Arial", 16)).pack(pady=20)
    return frame
