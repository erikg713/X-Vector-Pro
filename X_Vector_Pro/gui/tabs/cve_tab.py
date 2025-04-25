import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QProgressBar
from core.cve_lookup import find_exploits_for_cve

class CVETab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.cve_input = QLineEdit()
        self.cve_input.setPlaceholderText("e.g., CVE-2023-12345")

        self.search_button = QPushButton("Find Exploits")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Progress bar for showing loading state
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indeterminate state
        self.progress_bar.setVisible(False)

        layout.addWidget(QLabel("CVE ID:"))
        layout.addWidget(self.cve_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.search_button.clicked.connect(self.handle_lookup)

    def handle_lookup(self):
        cve_id = self.cve_input.text().strip()
        if not cve_id:
            self.output.setText("Please enter a CVE ID.")
            return

        if not re.match(r"^CVE-\d{4}-\d{4,}$", cve_id):
            self.output.setText("Invalid CVE format. Use e.g., CVE-2023-12345.")
            return

        # Clear output and show progress
        self.output.clear()
        self.progress_bar.setVisible(True)

        try:
            # Start searching for exploits
            self.output.setText("Searching...")
            results = find_exploits_for_cve(cve_id)

            # Format results for readability
            if results:
                formatted_results = self.format_results(results)
                self.output.setText(formatted_results)
            else:
                self.output.setText("No exploits found.")

        except Exception as e:
            self.output.setText(f"Error: {str(e)}")

        finally:
            self.progress_bar.setVisible(False)

    def format_results(self, results):
        """Helper method to format the exploit results."""
        formatted_results = ""
        for exploit in results:
            # Assuming `results` is a list of dictionaries or tuples with necessary fields
            formatted_results += f"Exploit Name: {exploit.get('name', 'N/A')}\n"
            formatted_results += f"Description: {exploit.get('description', 'N/A')}\n"
            formatted_results += f"Link: {exploit.get('link', 'N/A')}\n\n"
        return formatted_results
