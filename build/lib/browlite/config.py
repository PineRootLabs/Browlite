import os
import configparser
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.app_dir, 'config.ini')
        self._ensure_config()

    def _ensure_config(self):
        if not os.path.exists(self.config_path):
            self._create_default_config()

    def _create_default_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'homepage': 'https://www.google.com',
            'dark_mode': 'true',
            'block_ads': 'true',
            'default_search_engine': 'google'
        }
        with open(self.config_path, 'w') as f:
            config.write(f)

    def get_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config['DEFAULT']