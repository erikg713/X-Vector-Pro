import customtkinter as ctk

def show_splash_screen():
    splash = ctk.CTk()
    splash.geometry("400x200")
    splash.title("X-Vector Pro")
    ctk.CTkLabel(splash, text="Initializing X-Vector Pro...", font=("Arial", 18)).pack(pady=40)
    ctk.CTkLabel(splash, text="Silent. Adaptive. Lethal.", font=("Courier", 12)).pack()
    splash.after(2000, splash.destroy)  # Show for 2 seconds
    splash.mainloop()
