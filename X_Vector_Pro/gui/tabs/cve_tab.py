import re
import customtkinter as ctk
from core.cve_lookup import find_exploits_for_cve

class CVETab(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        layout = ctk.CTkFrame(self)

        # Create UI elements
        self.cve_input = ctk.CTkEntry(layout, width=400, placeholder_text="e.g., CVE-2023-12345")
        self.search_button = ctk.CTkButton(layout, text="Find Exploits", command=self.handle_lookup)
        self.output = ctk.CTkTextbox(layout, height=200, width=600, state="disabled")
        self.progress_bar = ctk.CTkProgressBar(layout, mode="indeterminate", width=400)
        self.progress_bar.grid(row=3, column=0, pady=10)
        
        # Label
        self.cve_label = ctk.CTkLabel(layout, text="Enter CVE ID:")
        
        # Place elements in grid
        self.cve_label.grid(row=0, column=0, padx=10, pady=5)
        self.cve_input.grid(row=1, column=0, padx=10, pady=5)
        self.search_button.grid(row=2, column=0, padx=10, pady=5)
        self.output.grid(row=4, column=0, padx=10, pady=10)

        # Layout Setup
        layout.pack(padx=20, pady=20)

    def handle_lookup(self):
        cve_id = self.cve_input.get().strip()
        if not cve_id:
            self.output.configure(state="normal")
            self.output.delete(1.0, "end")
            self.output.insert("end", "Please enter a CVE ID.")
            self.output.configure(state="disabled")
            return

        if not re.match(r"^CVE-\d{4}-\d{4,}$", cve_id):
            self.output.configure(state="normal")
            self.output.delete(1.0, "end")
            self.output.insert("end", "Invalid CVE format. Use e.g., CVE-2023-12345.")
            self.output.configure(state="disabled")
            return

        # Show progress bar
        self.output.configure(state="normal")
        self.output.delete(1.0, "end")
        self.output.insert("end", "Searching...")
        self.output.configure(state="disabled")
        self.progress_bar.start()

        # Start searching for exploits
        try:
            results = find_exploits_for_cve(cve_id)

            # Format results for readability
            self.output.configure(state="normal")
            self.output.delete(1.0, "end")

            if results:
                formatted_results = self.format_results(results)
                self.output.insert("end", formatted_results)
            else:
                self.output.insert("end", "No exploits found.")
        except Exception as e:
            self.output.insert("end", f"Error: {str(e)}")
        finally:
            self.output.configure(state="disabled")
            self.progress_bar.stop()

    def format_results(self, results):
        """Helper method to format the exploit results."""
        formatted_results = ""
        for exploit in results:
            formatted_results += f"Exploit Name: {exploit.get('name', 'N/A')}\n"
            formatted_results += f"Description: {exploit.get('description', 'N/A')}\n"
            formatted_results += f"Link: {exploit.get('link', 'N/A')}\n\n"
        return formatted_results
