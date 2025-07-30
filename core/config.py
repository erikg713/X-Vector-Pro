import json
import os

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')

class Config:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.settings = {}
        self.load()

    def load(self):
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
