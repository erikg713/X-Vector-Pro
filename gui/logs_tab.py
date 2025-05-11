import customtkinter as ctk

def logs_tab_widgets(tab):
    log_box = ctk.CTkTextbox(tab, height=20, width=80)
    log_box.pack(pady=10, padx=10)

    clear_logs_button = ctk.CTkButton(tab, text="Clear Logs", command=lambda: log_box.delete(1.0, "end"))
    clear_logs_button.pack(pady=10, padx=10)

    # You can add more log-specific functionalities here
