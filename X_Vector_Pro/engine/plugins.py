import json, re, requests

class PluginScanner:
    def __init__(self, url, logger):
        self.url = url
        self.log = logger
        self.found_plugins = []

    def run(self, findings):
        try:
            self.log("[*] Checking for plugins/themes...")
            r = requests.get(self.url, timeout=10)
            html = r.text
            with open("cve_db.json") as f:
                vuln_db = json.load(f)

            for plugin in vuln_db:
                if f"/wp-content/plugins/{plugin}" in html:
                    version_match = re.search(rf'/wp-content/plugins/{plugin}.*?[?&]ver=([\d\.]+)', html)
                    if version_match:
                        version = version_match.group(1)
                        if version in vuln_db[plugin]:
                            cve = vuln_db[plugin][version]
                            findings["cves"].append({
                                "plugin": plugin,
                                "version": version,
                                "cve": cve["cve"],
                                "desc": cve["desc"]
                            })
                            self.log(f"    [!!] {plugin} v{version} is vulnerable!")
                            self.log(f"         → {cve['desc']}")
                            self.found_plugins.append(cve["exploit"])
            if not self.found_plugins:
                self.log("    [-] No known vulnerable plugins found.")
        except Exception as e:
            self.log(f"[!] Plugin check failed: {e}")
        return self.found_plugins
