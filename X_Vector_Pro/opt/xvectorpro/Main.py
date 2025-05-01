# X_Vector_Pro/opt/xvectorpro/Main.py

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
