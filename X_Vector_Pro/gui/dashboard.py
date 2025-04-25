import sys
import os
import importlib
import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Dynamically discover and import all tabs in the `gui.tabs` package
TAB_CLASSES = {}

def load_tabs():
    tabs_package = "gui.tabs"  # Path to the tabs package (relative to this file)
    tabs_dir = os.path.join(os.path.dirname(__file__), "tabs")

    for module_name in os.listdir(tabs_dir):
        if module_name.endswith(".py") and module_name != "__init__.py":
            # Import the module dynamically
            module_path = f"{tabs_package}.{module_name[:-3]}"
            module = importlib.import_module(module_path)

            # Find all classes in the module that end with 'Tab' and add them to the TAB_CLASSES dictionary
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and attribute_name.endswith("Tab"):
                    TAB_CLASSES[attribute_name.replace("Tab", "")] = attribute

# Load all tabs dynamically
load_tabs()

# Ensure we have the required tabs in the TAB_CLASSES dictionary
if not TAB_CLASSES:
    raise Exception("No tabs found! Please check the tabs directory.")

# Toast Class for Toast Notification
class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, duration=2000):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(fg_color="#2e2e2e")
        self.geometry(f"250x40+{master.winfo_x() + 50}+{master.winfo_y() + 50}")
        label = ctk.CTkLabel(self, text=message, text_color="white")
        label.pack(padx=10, pady=5)
        self.after(duration, self.destroy)

def show_toast(master, message, duration=2000):
    Toast(master, message, duration)

# Dashboard Class for X-Vector Pro Interface
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("X-Vector Pro")
        self.geometry("1200x800")
        self.minsize(1024, 700)

        self.active_tab = None
        self.tab_instances = {}

        self.build_sidebar()
        self.build_main_area()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="X-Vector Pro", font=("Arial", 20, "bold")).pack(pady=20)

        for tab_name in TAB_CLASSES:
            ctk.CTkButton(
                self.sidebar,
                text=tab_name,
                command=lambda name=tab_name: self.switch_tab(name)
            ).pack(padx=10, pady=5, fill="x")

    def build_main_area(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")

    def switch_tab(self, tab_name):
        if self.active_tab:
            self.active_tab.pack_forget()

        # Gracefully handle invalid tab names
        if tab_name not in TAB_CLASSES:
            show_toast(self, f"Tab '{tab_name}' not found!", 2000)
            return

        if tab_name not in self.tab_instances:
            self.tab_instances[tab_name] = TAB_CLASSES[tab_name](self.content_frame)

        self.active_tab = self.tab_instances[tab_name]
        self.active_tab.pack(expand=True, fill="both")

# Run the Application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
