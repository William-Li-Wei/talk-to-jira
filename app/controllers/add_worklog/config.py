"""
    Config controller for add_worklog
"""

from app.controllers import config as conf


#  log <NUMBER> hours/minutes to ticket <ISSUE_KEY>
#  e.g. <ISSUE_KEY>: NI-1147

INPUT_GUIDE_REQUIRED_FIELDS = "Required fields missing, please provide them with the following pattern: \n" \
    + "'log <NUMBER> hours to issue <ISSUE_KEY>'\n" \
    + "e.g. 'log 3.5 hours to issue NI-1147'"
INPUT_GUIDE_OPTIONAL_COMMENT = "Regarding the optional fields, you can : \n" \
    + "- ADD COMMENT: 'with comment as <YOUR_COMMENT>'" \
    + "- SKIP COMMENT: 'skip comment'"


MIN_COMPLETE_PATTERN = r'log\s{number}\s{timeunit}\sto\sissue\s{issuekey}'.format(
    number=conf.COMMON_PATTERN_NUMBER,
    timeunit=conf.COMMON_PATTERN_TIMEUNIT,
    issuekey=conf.COMMON_PATTERN_ISSUEKEY
)

TRIGGER_PATTERNS = [
    MIN_COMPLETE_PATTERN,
    r'log my (time|work)'
]

PARAMS = {
    'issueKey': {
        'required': True,
        'type': str,
        'pattern': conf.COMMON_PATTERN_ISSUEKEY,
        'input_guide': INPUT_GUIDE_REQUIRED_FIELDS
    },
    'timeSpent': {
        'required': True,
        'type': str,
        'pattern': r'(?<=log\s){timespent}'.format(timespent=conf.COMMON_PATTERN_TIMESPENT),
        'input_guide': INPUT_GUIDE_REQUIRED_FIELDS
    },
    'comment': {
        'required': False,
        'type': str,
        'pattern': conf.COMMON_PATTERN_COMMENT,
        'input_guide': INPUT_GUIDE_REQUIRED_FIELDS,
        'skip_pattern': ['skip comment', 'skip all']
    }
}
