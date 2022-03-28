"""
This module is used for utility functions for the setup/startup of the client
"""

import yaml
from ...common.game_logic.states import State


def get_initial_game_state():
    return {
        'state': State.CALIBRATING
    }
