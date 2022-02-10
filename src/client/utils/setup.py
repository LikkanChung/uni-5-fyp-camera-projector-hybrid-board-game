"""
This module is used for utility functions for the setup/startup of the client
"""

import yaml
from ...common.game_logic.states import State

CONFIG_FILE = 'src/client/config.yaml'


def load_config():
    with open(CONFIG_FILE, 'r', encoding='UTF-8') as config_file:
        return yaml.safe_load(config_file)

def get_initial_game_state():
    return {
        'state': State.CALIBRATING
    }
