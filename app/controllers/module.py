
import importlib
import re

from abc import ABC, abstractmethod


class BaseController(ABC):
    @property
    def config(self):
        return self.__config

    def __init__(self):
        """
            sets config for the child controller.
            the config module(`config.py`) is located in the same package as the child controller module(`module.py`)
        """
        _package = self.__module__[: self.__module__.rindex('.')]
        _config_path = _package + '.config'
        _config_module = importlib.import_module(_config_path)
        self.__config = _config_module.controller_settings


    def respond_to_trigger(self, trigger: str):
        """
        checks if this controller should respond to the trigger message

        Args:
            trigger(str): the trigger message

        Returns:
            True, if the trigger match any pattern, else False
        """
        for pattern in self.config['trigger_patterns']:
            m = re.search(pattern, trigger)
            return m is not None
