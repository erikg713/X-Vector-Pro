import json
import os

class CVEChecker:
    def __init__(self, cve_db_path=None):
        if not cve_db_path:
            cve_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cve_db.json')
        self.cve_db_path = cve_db_path
        self.cve_data = self.load_cve_db()

    def load_cve_db(self):
        try:
            with open(self.cve_db_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def check_plugins(self, plugins):
        results = {}
        for plugin, version in plugins.items():
            vulns = self.cve_data.get(plugin, {})
            vuln_list = []
            for cve, info in vulns.items():
                if version >= info.get("vulnerable_from", "") and version <= info.get("vulnerable_to", ""):
                    vuln_list.append(cve)
            if vuln_list:
                results[plugin] = vuln_list
        return results
