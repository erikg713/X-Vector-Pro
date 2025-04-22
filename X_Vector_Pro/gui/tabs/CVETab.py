from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from core.exploit_lookup import find_exploits_for_cve  # make this in core

class CVETab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.cve_input = QLineEdit()
        self.cve_input.setPlaceholderText("e.g., CVE-2023-1234")
        self.search_button = QPushButton("Find Exploits")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(QLabel("CVE ID:"))
        layout.addWidget(self.cve_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.handle_lookup)

    def handle_lookup(self):
        cve = self.cve_input.text().strip()
        if not cve:
            self.output.setText("Please enter a CVE ID.")
            return
        self.output.setText("Searching...")
        try:
            results = find_exploits_for_cve(cve)
            self.output.setText(results)
        except Exception as e:
            self.output.setText(f"Error: {str(e)}")
