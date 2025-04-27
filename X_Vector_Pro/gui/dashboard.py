# gui/dashboard.py

import os
import sys
import importlib
import customtkinter as ctk
import json

# Load config.json
DATA_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(DATA_DIR, 'config.json')

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Example usage:
if config.get("stealth_mode"):
    print("Stealth mode is ON!")
# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Dynamically discover and import all tabs
TAB_CLASSES = {}

def load_tabs():
    tabs_package = "gui.tabs"
    tabs_dir = os.path.join(os.path.dirname(__file__), "tabs")

    for module_name in os.listdir(tabs_dir):
        if module_name.endswith(".py") and module_name != "__init__.py":
            module_path = f"{tabs_package}.{module_name[:-3]}"
            module = importlib.import_module(module_path)

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and attribute_name.endswith("Tab"):
                    TAB_CLASSES[attribute_name.replace("Tab", "")] = attribute

# Load available tabs at startup
load_tabs()

if not TAB_CLASSES:
    raise Exception("No tabs found! Please check the 'tabs' directory.")

# Toast Notification
class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, duration=2000):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(fg_color="#2e2e2e")
        x = master.winfo_rootx() + 100
        y = master.winfo_rooty() + 80
        self.geometry(f"250x50+{x}+{y}")

        label = ctk.CTkLabel(self, text=message, text_color="white")
        label.pack(expand=True, padx=10, pady=10)

        self.after(duration, self.destroy)

def show_toast(master, message, duration=2000):
    Toast(master, message, duration)

# Main Dashboard Class
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1200x800")
        self.minsize(1024, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.active_tab = None
        self.tab_instances = {}

        self.build_sidebar()
        self.build_main_area()

        # Load default tab
        default_tab = next(iter(TAB_CLASSES))
        self.switch_tab(default_tab)

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        title = ctk.CTkLabel(
            self.sidebar,
            text="X-Vector Pro",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        title.pack(pady=(30, 20))

        for tab_name in TAB_CLASSES:
            button = ctk.CTkButton(
                self.sidebar,
                text=tab_name,
                command=lambda name=tab_name: self.switch_tab(name),
                fg_color="#2b2b2b",
                hover_color="#3c3c3c"
            )
            button.pack(padx=15, pady=7, fill="x")

    def build_main_area(self):
        self.content_frame = ctk.CTkFrame(self, fg_color="#121212")
        self.content_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    def switch_tab(self, tab_name):
        if self.active_tab:
            self.active_tab.pack_forget()

        if tab_name not in TAB_CLASSES:
            show_toast(self, f"Tab '{tab_name}' not found!")
            return

        if tab_name not in self.tab_instances:
            self.tab_instances[tab_name] = TAB_CLASSES[tab_name](self.content_frame)

        self.active_tab = self.tab_instances[tab_name]
        self.active_tab.pack(expand=True, fill="both")

# Run the Application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
