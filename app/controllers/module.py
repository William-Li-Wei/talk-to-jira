
import importlib
import re
from abc import ABC
from collections import OrderedDict

import config as app_conf
from app import data_io



class BaseController(ABC):
    """
    BaseController as an abstract class, is the base of all actual controllers.
    It has the following properties:

    self.active: bool property that indicates if the current controller is activated, set by config
    self.mode: running mode from ['microphone', 'keyboard', 'api'], default to 'microphone'
    - microphone mode would interact witht the microphone
    - keyboard mode would interact witht the keyboard
    - api mode would interact through the http REST APIs with sessions

    self.trigger_patterns: activate the controller if any patterns found in the input trigger message, set by config
    self.params: dictionary with JIRA params as keys, set by config

    """

    BASE_URL = app_conf.DOMAIN
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + app_conf.AUTH_HEADER
    }

    mandatory_properties = [
        'trigger_patterns',
        'params'
    ]


    def prepare_url_and_req_body(self):
        """
        placehoder for prepare_url_and_req_body function.
        This should be implemented in the actual child controller.

        process the input params, compose the url and request body
        """
        raise NotImplementedError


    def call_jira(self):
        """
        placehoder for call_jira function.
        This should be implemented in the actual child controller
        """
        raise NotImplementedError


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
        if not set(self.mandatory_properties).issubset(set(_config_module.controller_properties.keys())):
            _message = "[Controller config error]. Not all mandatory properties are present:{} " \
                .format(str(self.mandatory_properties))
            raise Exception(_message)

        #  set controller's properties
        for k, v in _config_module.controller_properties.items():
            if isinstance(v, dict):
                setattr(self, k, OrderedDict(v))
            else:
                setattr(self, k, v)


    def __update_multiple_params(self, user_input: str):
        """
        tries to update all params with the matched pattern and sets their fufillments to True

        Args:
            user_input(str): user input

        """

        if not user_input:
            return

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

        if not user_input:
            return

        start_over = re.search(param.get('start_over_command'), user_input) is not None

        if start_over:
            for k, v in self.params.items():
                v['fulfilled'] = False
                v['skipped'] = False
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
                    param['value'] = param.get('dtype')(match.group())
                    param['fulfilled'] = True


    def __list_unfulfilled_params(self):
        return [v for k, v in self.params.items() if (not v.get('fulfilled')) and (not v.get('skipped'))]


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
        # collect input for JIRA action
        if self.mode == 'api':
            self.collect_params_in_api_mode(user_input)
        else:
            self.collect_params_in_local_mode()

        # all input params collected, process them for Jira format
        self.prepare_url_and_req_body()

        # all params processed, call Jira
        self.call_jira()


    def collect_params_in_api_mode(self, user_input: str):
        """
        collect necessary data in api mode

        Args:
            user_input(str):

        Returns:
        """
        unfilfulled_params = self.__list_unfulfilled_params()
        param = unfilfulled_params[0]

        self.__update_param(param, user_input)

        unfilfulled_params = self.__list_unfulfilled_params()
        # TODO: logic to collect params in api mode
        #  if not unfilfulled_params:


    def collect_params_in_local_mode(self):
        """
        collect necessary data in local mode
        """
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
