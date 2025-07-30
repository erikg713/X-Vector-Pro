import requests

class PluginScanner:
    def __init__(self, target):
        self.target = target.rstrip('/')

    def run(self):
        plugins = {}
        # Example: check for plugin readme file
        known_plugins = ['akismet', 'jetpack', 'wordpress-seo']
        for plugin in known_plugins:
            url = f"{self.target}/wp-content/plugins/{plugin}/readme.txt"
            try:
                resp = requests.get(url, timeout=3)
                if resp.status_code == 200:
                    version = self._parse_version(resp.text)
                    plugins[plugin] = version
            except Exception:
                continue
        return plugins

    def _parse_version(self, text):
        for line in text.splitlines():
            if line.lower().startswith('stable tag:'):
                return line.split(':')[1].strip()
        return "unknown"
