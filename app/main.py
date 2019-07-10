"""
    Entrypoint
"""


import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.insert(0, project_root)

from app import dispatch
from app import data_io


if __name__ == "__main__":
    print("let's talk to jira")

    mode = 'microphone'
    # mode = 'keyboard'

    controller = None

    while not controller:
        trigger = None
        if mode == 'microphone':
            trigger = data_io.read_from_microphone()
        if mode == 'keyboard':
            trigger = data_io.read_from_keyboard()

        controller = dispatch.get_controller_by_trigger(trigger, 'microphone')

    controller.run_pipeline()
    tmp = [(k, v.get('value')) for k, v in controller.params.items()]
    print(tmp)

