"""
    Config AddWorklogController
"""

from app.controllers import config as common_conf


CONTROLLER_NAME = 'AddWorklogController'

#  log <NUMBER> hours/minutes to ticket <ISSUE_KEY>
#  e.g. <ISSUE_KEY>: NI-1147

INPUT_GUIDE = "Required fields missing, please provide them witht he following pattern: \n" \
    + "log <NUMBER> hours to issue <ISSUE_KEY> \n" \
    + "e.g. 'log 3.5 hours to issue NI-1147'"

MIN_COMPLETE_PATTERN = r'log\s{number}\s{timeunit}\sto\sissue\s{issuekey}'.format(
    number=common_conf.COMMON_PATTERN_NUMBER,
    timeunit=common_conf.COMMON_PATTERN_TIMEUNIT,
    issuekey=common_conf.COMMON_PATTERN_ISSUEKEY
)

TRIGGER_PATTERNS = [
    MIN_COMPLETE_PATTERN,
    r'log my (time|work)'
]

PARAMS = {
    'issueKey': {
        'required': True,
        'type': str,
        'pattern': common_conf.COMMON_PATTERN_ISSUEKEY
    },
    'timeSpent': {
        'required': True,
        'type': str,
        'pattern': r'(?=log\s){number}\s{timeunit}'.format(
            number=common_conf.COMMON_PATTERN_NUMBER,
            timeunit=common_conf.COMMON_PATTERN_TIMEUNIT
        )
    },
    'comment': {
        'required': False,
        'type': str,
        'pattern': common_conf.COMMON_PATTERN_COMMENT
    }
}
