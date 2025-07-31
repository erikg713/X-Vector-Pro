import requests
from core.logger import log_event

class PluginScanner:
    def __init__(self, target):
        self.target = target
        self.plugins = {}

    def detect_plugins(self):
        # Dummy logic: checks common plugin URLs and returns version if found
        common_plugins = {
            'akismet': 'https://{}/wp-content/plugins/akismet/readme.txt',
            'yoast-seo': 'https://{}/wp-content/plugins/wordpress-seo/readme.txt',
        }

        found_plugins = {}

        for plugin, url_template in common_plugins.items():
            url = url_template.format(self.target)
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    # Extract version line (simple heuristic)
                    for line in resp.text.splitlines():
                        if 'Stable tag:' in line:
                            version = line.split(':')[1].strip()
                            found_plugins[plugin] = version
                            break
                    else:
                        found_plugins[plugin] = 'unknown'
                    log_event("scan", {"action": "plugin_detected", "plugin": plugin, "version": found_plugins[plugin]})
            except Exception as e:
                log_event("scan", {"action": "plugin_check_failed", "plugin": plugin, "error": str(e)}, level="error")

        self.plugins = found_plugins
        return found_plugins

    def scan(self):
        return self.detect_plugins()


if __name__ == "__main__":
    scanner = PluginScanner("example.com")
    results = scanner.scan()
    print("Detected plugins:", results)
