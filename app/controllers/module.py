
import importlib
import re

from abc import ABC

from app import data_io


class BaseController(ABC):
    """
    BaseController as an abstract class, is the base of all actual controllers.
    It has the following properties:

    self.active: bool property that indicates if the current controller is activated, set by config
    self.mode: running mode from ['microphone', 'keyboard', 'api'], default to 'microphone'
    - local mode would interact witht the microphone
    - keyboard mode would interact witht the keyboard
    - api mode would interact through the http REST APIs with sessions

    self.trigger_patterns: activate the controller if any patterns found in the input trigger message, set by config
    self.params: dictionary with JIRA params as keys, set by config

    """

    __mandatory_properties = [
        'trigger_patterns',
        'params'
    ]

    def __init__(self, trigger: str, mode: str = 'microphone'):
        """
        initialize the controller with these steps:

        1. set controller's properties
        2. activate the controller if it matches the trigger
        3. update params if actived

        Args:
            trigger(str): the input trigger message

        """

        self.mode = mode
        self.__set_controller_properties()

        #  update controller's active flag
        for pattern in self.trigger_patterns:
            self.active = re.search(pattern, trigger) is not None
            if self.active:
                break

        #  update params according to the trigger message
        if self.active:
            self.__update_multiple_params(trigger)

    def __set_controller_properties(self):
        """
        sets controller's properties according to it's config file

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

    def __update_multiple_params(self, user_input: str):
        """
        tries to update all params with the matched pattern and sets their fufillments to True

        Args:
            user_input(str): user input

        """

        unfulfilled = self.__list_unfulfilled_params()

        for param in unfulfilled:
            self.__update_param(param, user_input)

    def __update_param(self, param: dict, user_input: str):
        """
        update the target param with the matched pattern and set its fulfillment to True

        Args:
            param(dict): the target parameter to update
            user_input(str): user input

        """

        start_over = re.search(param.get('start_over_command'), user_input) is not None

        if start_over:
            for p in self.params:
                p['fulfilled'] = False
                p['skipped'] = False
        else:
            if not param.get('required'):
                for cmd in param.get('skip_commands'):
                    skipped = re.search(cmd, user_input) is not None
                    if skipped:
                        param['skipped'] = True
                        break

            if not param.get('skipped'):
                match = re.search(param.get('pattern'), user_input)
                if match:
                    param['value'] = match.group()
                    param['fulfilled'] = True

    def __list_unfulfilled_params(self):
        return [p for p in self.params if (not p.get('fulfilled')) and (not p.get('skipped'))]

    def __interact_with_message(self, message: str):
        """
        __interact_with_message

        Args:
                message(str):

        Returns:
        """
        user_input = None

        if self.mode == 'microphone':
            user_input = data_io.read_from_microphone(message)

        if self.mode == 'keyboard':
            user_input = data_io.read_from_keyboard(message)

        return user_input

    def run_pipeline(self, user_input: str = None):
        """
        run_pipeline

        Args:
                user_input(str):

        Returns:
        """
        if self.mode == 'api':
            self.run_pipeline_in_api_mode(user_input)
        else:
            self.run_pipeline_in_local_mode()

        #  TODO: compose JIRA COMMAND

    def run_pipeline_in_api_mode(self, user_input: str):
        """
        run_pipeline_in_api_mode

        Args:
            user_input(str):

        Returns:
        """
        unfilfulled_params = self.__list_unfulfilled_params()
        param = unfilfulled_params[0]

        self.__update_param(param, user_input)

        unfilfulled_params = self.__list_unfulfilled_params()
        #  if not unfilfulled_params:

    def run_pipeline_in_local_mode(self):
        """run_pipeline_in_local_mode"""
        #  for microphone and keyboard mode
        while True:
            unfilfulled_params = self.__list_unfulfilled_params()
            if not unfilfulled_params:
                break

            param = unfilfulled_params[0]
            user_input = self.__interact_with_message(param.get('input_guide'))

            #  tried to match all required params with one sentence, using the MIN_COMPLETE_PATTERN
            #  maybe maching some optional params as well
            if param.get('required'):
                self.__update_multiple_params(user_input)
            #  tried to match optional params one by one
            else:
                self.__update_param(param, user_input)
