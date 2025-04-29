# main.py
import customtkinter as ctk
import traceback
from tkinter import messagebox
from gui.dashboard import launch_dashboard
from ui.tabs_directory import load_directory_tab
...
directory_tab = ctk.CTkFrame(tabview)
tabview.add(directory_tab, text="Directory Scan")
load_directory_tab(directory_tab)
def main():
    try:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        launch_dashboard()
    except Exception as e:
        error_msg = traceback.format_exc()
        print(error_msg)
        messagebox.showerror("Application Error", f"Something went wrong:\n\n{str(e)}")

if __name__ == "__main__":
    main()
