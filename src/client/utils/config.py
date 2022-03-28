"""
Configuration holding object
"""
import yaml
from cv2 import FONT_HERSHEY_SIMPLEX

CONFIG_FILE = 'src/client/config.yaml'


class Config:
    def __init__(self):
        self.config = dict()
        with open(CONFIG_FILE, 'r', encoding='UTF-8') as config_file:
            self.config = yaml.safe_load(config_file)
        self.global_pygame_font = None
        self.global_cv2_font = None

    def get_config(self):
        return self.config

    def get_property(self, key_list: list):
        """
        Allows getting the value from the config from a list of their properties
        :param key_list:
        :return: the value of the key
        """
        parsed_config = self.config
        for key in key_list:
            value = parsed_config.get(key)
            if value is None:
                return None
            else:
                parsed_config = value
        return parsed_config

    def set_global_pygame_font(self, font):
        self.global_pygame_font = font

    def get_global_pygame_font(self):
        return self.global_pygame_font

    def get_global_cv2_font(self):
        return self.global_cv2_font or FONT_HERSHEY_SIMPLEX

config = Config()
