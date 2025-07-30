from gui.tabs.tor_tab import TorTab
self.tabs["Tor"] = TorTab(self.tabview)
self.tabview.add("Tor", self.tabs["Tor"])
Here is the full implementation of `gui/gui.py` for your Sentenial-X platform, designed using `PyQt5` and integrated with backend modules for threat display, controls, and logs:

```python
# gui/gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QTabWidget, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer
from sentenial_core.orchestrator.incident_queue import IncidentQueue
from sentenial_core.simulator.synthetic_attack_fuzzer import SyntheticAttackFuzzer
from sentenial_core.cortex.intel_analyzer import BERTIntelAnalyzer
from sentenial_core.interfaces.logger import log_event
import datetime

class SentenialXGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentenial X - Autonomous Cyber Defense GUI")
        self.setGeometry(100, 100, 1200, 800)

        self.incident_queue = IncidentQueue()
        self.fuzzer = SyntheticAttackFuzzer()
        self.analyzer = BERTIntelAnalyzer()

        self.init_ui()
        self.init_timer()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: Threat Monitor
        self.monitor_tab = QWidget()
        self.monitor_layout = QVBoxLayout()

        self.threat_log = QTextEdit()
        self.threat_log.setReadOnly(True)
        self.monitor_layout.addWidget(QLabel("📡 Threat Feed"))
        self.monitor_layout.addWidget(self.threat_log)

        self.monitor_tab.setLayout(self.monitor_layout)
        self.tabs.addTab(self.monitor_tab, "Threat Monitor")

        # Tab 2: Intel Analyzer
        self.analyzer_tab = QWidget()
        self.analyzer_layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.analyze_button = QPushButton("Analyze Intel")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)

        self.analyze_button.clicked.connect(self.run_intel_analysis)

        self.analyzer_layout.addWidget(QLabel("🔍 Input Suspicious Log or Message"))
        self.analyzer_layout.addWidget(self.input_text)
        self.analyzer_layout.addWidget(self.analyze_button)
        self.analyzer_layout.addWidget(QLabel("🧠 Analysis Output"))
        self.analyzer_layout.addWidget(self.analysis_output)

        self.analyzer_tab.setLayout(self.analyzer_layout)
        self.tabs.addTab(self.analyzer_tab, "Intel Analyzer")

        # Tab 3: Red Team Fuzzer
        self.fuzzer_tab = QWidget()
        self.fuzzer_layout = QVBoxLayout()

        self.fuzz_button = QPushButton("Launch Synthetic Attack")
        self.fuzz_log = QTextEdit()
        self.fuzz_log.setReadOnly(True)

        self.fuzz_button.clicked.connect(self.run_fuzzer)

        self.fuzzer_layout.addWidget(QLabel("💣 Synthetic Attack Fuzzer"))
        self.fuzzer_layout.addWidget(self.fuzz_button)
        self.fuzzer_layout.addWidget(self.fuzz_log)

        self.fuzzer_tab.setLayout(self.fuzzer_layout)
        self.tabs.addTab(self.fuzzer_tab, "Attack Fuzzer")

        # Tab 4: Incident Log
        self.incidents_tab = QWidget()
        self.incidents_layout = QVBoxLayout()

        self.incident_list = QListWidget()
        self.refresh_incidents_button = QPushButton("Refresh Incidents")
        self.refresh_incidents_button.clicked.connect(self.load_incidents)

        self.incidents_layout.addWidget(QLabel("📄 Incident Queue"))
        self.incidents_layout.addWidget(self.incident_list)
        self.incidents_layout.addWidget(self.refresh_incidents_button)

        self.incidents_tab.setLayout(self.incidents_layout)
        self.tabs.addTab(self.incidents_tab, "Incident Log")

    def init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(5000)  # check every 5 seconds
        self.timer.timeout.connect(self.update_threat_feed)
        self.timer.start()

    def update_threat_feed(self):
        events = self.incident_queue.get_all()
        self.threat_log.clear()
        for e in events[-50:]:
            ts = e.get('timestamp', str(datetime.datetime.utcnow()))
            msg = e.get('message', 'Unknown event')
            level = e.get('severity', 'INFO')
            self.threat_log.append(f"[{ts}] ({level}) {msg}")

    def run_intel_analysis(self):
        text = self.input_text.toPlainText()
        if not text.strip():
            self.analysis_output.setPlainText("Please input a message for analysis.")
            return
        result = self.analyzer.analyze(text)
        self.analysis_output.setPlainText(str(result))

    def run_fuzzer(self):
        attack = self.fuzzer.generate()
        self.fuzz_log.append(f"Generated: {attack['description']}")
        log_event("Synthetic attack launched", severity="SIMULATION", data=attack)

    def load_incidents(self):
        self.incident_list.clear()
        events = self.incident_queue.get_all()
        for e in events[-100:]:
            item_text = f"{e.get('timestamp')} - {e.get('message')} [{e.get('severity')}]"
            QListWidgetItem(item_text, self.incident_list)

def main():
    app = QApplication(sys.argv)
    window = SentenialXGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

---

### 🔧 Features Implemented:

* **Tabs:** Modular display: *Threat Monitor*, *Intel Analyzer (BERT)*, *Attack Fuzzer*, *Incident Log*.
* **Live updates:** Background `QTimer` auto-refreshes threat log.
* **Simulated attacks:** Launch synthetic fuzzing via GUI.
* **NLP intent detection:** Real-time BERT classification from GUI.
* **Incident logging + viewer:** Pulls logs from backend `incident_queue`.

---

Would you like:

* A **dark theme**?
* **Log file saving**?
* **Live PiNet log stream** via WebSocket into the Threat Feed?

Let me know if we should Dockerize this GUI as a service or bundle it into the existing system.
