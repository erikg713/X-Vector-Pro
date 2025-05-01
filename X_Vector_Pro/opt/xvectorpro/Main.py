def start_gui():
    """
    Starts the X-Vector Pro GUI using customtkinter.

    This function initializes and runs the main GUI loop for the customtkinter application.
    """
    import customtkinter as ctk
    try:
        from .MainWindow import MainWindow  # Relative import if possible
    except ImportError:
        from MainWindow import MainWindow   # Fallback for direct run

    app = MainWindow()
    app.mainloop()import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("800x600")
        # Add your widgets and layout here
        label = ctk.CTkLabel(self, text="Welcome to X-Vector Pro!")
        label.pack(padx=20, pady=20)# X_Vector_Pro/opt/xvectorpro/Main.py

import os
import sys
import time
import traceback
from tkinter import Tk, TclError

from ui import dashboard_instance, toast_manager
from utils.logger import log_event

def start_gui():
    try:
        log_event("Launching X-Vector Pro GUI...")
        root = Tk()
        root.title("X-Vector Pro - Cyber Recon Toolkit")
        root.geometry("1200x800")
        root.configure(bg="#1e1e1e")

        dashboard_instance.inject(root)
        toast_manager.attach(root)

        root.mainloop()

    except TclError as e:
        log_event("FATAL GUI ERROR", level="ERROR")
        traceback.print_exc()
        sys.exit(1)

    except Exception as ex:
        log_event(f"Unexpected crash: {str(ex)}", level="CRITICAL")
        traceback.print_exc()
        time.sleep(3)
        sys.exit(1)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    start_gui()
