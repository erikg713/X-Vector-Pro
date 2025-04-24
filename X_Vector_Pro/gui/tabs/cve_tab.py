import os
import re

def handle_lookup(self):
    cve_id = self.cve_input.text().strip()
    if not cve_id:
        self.output.setText("Please enter a CVE ID.")
        return

    if not re.match(r"^CVE-\d{4}-\d{4,}$", cve_id):
        self.output.setText("Invalid CVE format. Use e.g., CVE-2023-12345.")
        return

    self.output.setText("Searching...")
    try:
        results = find_exploits_for_cve(cve_id)
        self.output.setText(results)
    except Exception as e:
        self.output.setText(f"Error: {str(e)}")

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
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

        layout.addWidget(QLabel("CVE ID:"))
        layout.addWidget(self.cve_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.search_button.clicked.connect(self.handle_lookup)

    def handle_lookup(self):
        cve_id = self.cve_input.text().strip()
        if not cve_id:
            self.output.setText("Please enter a CVE ID.")
            return

        self.output.setText("Searching...")
        try:
            results = find_exploits_for_cve(cve_id)
            self.output.setText(results)
        except Exception as e:
            self.output.setText(f"Error: {str(e)}")
