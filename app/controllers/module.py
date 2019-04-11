
import importlib
import re

from abc import ABC


class BaseController(ABC):

    __mandatory_properties = [
        'trigger_patterns',
        'active',
        'params'
    ]

    def __init__(self, trigger: str):
        """
        initialize the controller with these steps:

        1. set controller's properties
        2. activate the controller if it matches the trigger
        3. update params if active

        Args:
            trigger(str):

        """

        self.__set_controller_properties()

        #  update controller's active flag
        for pattern in self.trigger_patterns:
            self.active = self.active or (re.search(pattern, trigger) is not None)

        #  update params according to the trigger message
        if self.active:
            self.update_params(trigger)

    def __set_controller_properties(self):
        """
        sets controller's properties:

        1. fulfillment check for the mandatory properties
        2. setup properties according to actual controller's config file

        the config module(`config.py`) is located in the same package as the child controller module(`module.py`)
        """

        #  load controller's config file
        _package = self.__module__[: self.__module__.rindex('.')]
        _config_path = _package + '.config'
        _config_module = importlib.import_module(_config_path)

        #  mandatory properties check
        if not set(self.__mandatory_properties).issubset(set(_config_module.controller_properties.keys())):
            _message = "Not all mandatory properties are present in the controller's config file:{} " \
                .format(str(self.__mandatory_properties))
            raise Exception(_message)

        #  set controller's properties
        for key, value in _config_module.controller_properties.items():
            setattr(self, key, value)

    def update_params(self, message: str):
        for param in self.params:
            match = re.search(param['pattern'], message)
            if match:
                param['value'] = match.group()

    def run_pipeline(self, message: str):
        self.update_params(message)
