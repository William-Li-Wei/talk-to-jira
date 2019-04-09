"""
   Configuration for all controllers
"""


COMMON_PATTERN_NUMBER = r'(\d+\.\d+|\d+)'
COMMON_PATTERN_TIMEUNIT = r'(days?|hours?|minutes?)'
COMMON_PATTERN_TIMESPENT = r'{number}\s{timeunit}'.format(
    number=COMMON_PATTERN_NUMBER,
    timeunit=COMMON_PATTERN_TIMEUNIT
)
COMMON_PATTERN_ISSUEKEY = r'(?<=issue\s)[a-z]+\-\d+'
COMMON_PATTERN_COMMENT = r'(?<=with\scomment\sas\s).*'
