"""
    Entrypoint
"""


import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.insert(0, project_root)


#  from app.controllers.worklog import WorklogController
#  from app import data_io
from app import dispatch


if __name__ == "__main__":
    print("let's talk to jira")

    # issue_key = 'TTJ-1'
    # comment = 'posted worklog via JIRA API'
    # time_spent_seconds = 2 * 60 * 60

    # worklog_ctl = WorklogController()
    # res = worklog_ctl.add_worklog(issue_key, time_spent_seconds, comment)

    # print(res.text)

    #  audio = data_io.record_audio_from_microphone()
    #  text = data_io.recognize_speech_from_audio(audio)
    #  print(text)

    #  trigger = "log 3.5 hours to issue NI-779 with comment as i hate this issue"
    trigger = "log my work"
    controller = dispatch.get_controller_by_trigger(trigger, 'keyboard')
    if controller:
        controller.run_pipeline()
        print(controller.params)
