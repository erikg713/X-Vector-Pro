import customtkinter as ctk

def show_toast(message, duration=3, style="info"):
    toast = ctk.CTkToplevel()
    toast.overrideredirect(True)
    toast.geometry("300x50+60+60")
    toast.attributes("-topmost", True)

    colors = {
        "info": "#1E90FF",
        "success": "#28a745",
        "error": "#dc3545"
    }

    frame = ctk.CTkFrame(toast, fg_color=colors.get(style, "#1E90FF"))
    frame.pack(fill="both", expand=True)
    label = ctk.CTkLabel(frame, text=message, text_color="white", font=("Arial", 14))
    label.pack(pady=10)

    toast.after(duration * 1000, toast.destroy)
