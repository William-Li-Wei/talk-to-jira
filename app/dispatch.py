import importlib
import os

from pathlib import Path


def get_controller_by_trigger(trigger: str, mode: str = 'microphone'):
    """
    damically returns a specific controller that matches the trigger message's intention

    Args:
        trigger(str): the initial input indicating the intention

    Returns:
        controller: instance of the matched controller class
    """

    activated_controller = None

    #  locate module.py of all actual controllers
    base_path = Path(os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controllers/')))
    module_files = list(base_path.glob('*/module.py'))

    #  import each actual controler
    for module_file in module_files:

        #  import controller module from string
        module_path = os.path.dirname(os.path.relpath(module_file)) \
            .replace('/', '.') + '.module'
        module = importlib.import_module(module_path)

        #  instanciate the controller
        controller = module.Controller(trigger, mode)

        if controller.active:
            activated_controller = controller
            break

    return activated_controller
