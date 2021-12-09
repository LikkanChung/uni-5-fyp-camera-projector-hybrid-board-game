"""
This module is used for utility functions for the setup/startup of the client
"""

import yaml


CONFIG_FILE = 'src/client/config.yaml'


def load_config():
    with open(CONFIG_FILE, 'r', encoding='UTF-8') as config_file:
        return yaml.safe_load(config_file)