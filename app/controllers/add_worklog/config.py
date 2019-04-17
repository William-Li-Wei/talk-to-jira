"""
    Config controller for add_worklog
"""

from app.controllers import config as base_conf


MIN_COMPLETE_PATTERN = r'log\s{number}\s{timeunit}\sto\sissue\s{issuekey}'.format(
    number=base_conf.COMMON_PATTERN_NUMBER,
    timeunit=base_conf.COMMON_PATTERN_TIMEUNIT,
    issuekey=base_conf.COMMON_PATTERN_ISSUEKEY
)
MIN_COMPLETE_PATTERN_READABLE = 'log <NUMBER> hours to issue <ISSUE_KEY>'
MIN_COMPLETE_PATTERN_EXAMPLE = 'log 3.5 hours to issue NI-1147'

INPUT_GUIDE_REQUIRED_PARAMS = base_conf.get_inputguide_required_params(
    MIN_COMPLETE_PATTERN_READABLE,
    MIN_COMPLETE_PATTERN_EXAMPLE,
    base_conf.COMMON_COMMAND_STARTOVER_READABLE
)

controller_properties = {
    'params': [
        {
            'name': 'issueKey',
            'required': True,
            'type': str,
            'pattern': base_conf.COMMON_PATTERN_ISSUEKEY,
            'input_guide': INPUT_GUIDE_REQUIRED_PARAMS,
            'start_over_command': base_conf.COMMON_COMMAND_STARTOVER
        },
        {
            'name': 'timeSpent',
            'required': True,
            'type': str,
            'pattern': r'(?<=log\s){timespent}'.format(timespent=base_conf.COMMON_PATTERN_TIMESPENT),
            'input_guide': INPUT_GUIDE_REQUIRED_PARAMS,
            'start_over_command': base_conf.COMMON_COMMAND_STARTOVER
        },
        {
            'name': 'comment',
            'required': False,
            'type': str,
            'pattern': base_conf.COMMON_PATTERN_COMMENT,
            'input_guide': base_conf.get_inputguide_optional_param(
                'comment',
                base_conf.COMMON_PATTERN_COMMENT_READABLE,
                base_conf.COMMON_COMMAND_SKIP_IT_READABLE,
                base_conf.COMMON_COMMAND_SKIP_ALL_READABLE,
                base_conf.COMMON_COMMAND_STARTOVER_READABLE
            ),
            'start_over_command': base_conf.COMMON_COMMAND_STARTOVER,
            'skip_commands': [base_conf.COMMON_COMMAND_SKIP_ALL, base_conf.COMMON_COMMAND_SKIP_IT]
        }
    ],
    'trigger_patterns': [
        MIN_COMPLETE_PATTERN,
        r'log my (time|work)'
    ]
}
