"""
   Configuration for all controllers
"""
#  re patterns for common used params
COMMON_PATTERN_NUMBER = r'(\d+\.\d+|\d+)'
COMMON_PATTERN_NUMBER_READABLE = '<NUMBER>'

COMMON_PATTERN_TIMEUNIT = r'(day?s?|hour?s?|minute?s?)'
COMMON_PATTERN_TIMEUNIT_READABLE = '<DAYS or HOURS or MINUTES>'

COMMON_PATTERN_TIMESPENT = r'{number}\s{timeunit}' \
    .format(number=COMMON_PATTERN_NUMBER, timeunit=COMMON_PATTERN_TIMEUNIT)
COMMON_PATTERN_TIMESPENT_READABLE = '<NUMBER> <DAYS or HOURS or MINUTES>'

COMMON_PATTERN_ISSUEKEY = r'(?<=issue\s)[a-zA-Z]+[\-\s]*\d+'
COMMON_PATTERN_ISSUEKEY_READABLE = 'issue <ISSUE_KEY>'

COMMON_PATTERN_COMMENT = r'(?<=with\scomment\sas\s).*'
COMMON_PATTERN_COMMENT_READABLE = 'with comment as <YOUR COMMENT>'

#  re patterns for common commands
COMMON_COMMAND_STARTOVER = r'^start\sover'
COMMON_COMMAND_STARTOVER_READABLE = 'start over'

COMMON_COMMAND_SKIP_IT = r'^skip\sit'
COMMON_COMMAND_SKIP_IT_READABLE = 'skip it'

COMMON_COMMAND_SKIP_ALL = r'^skip\sall'
COMMON_COMMAND_SKIP_ALL_READABLE = 'skip all'


#  standard input guides
INPUT_GUIDE_REQUIRED_PARAMS_TEMPLATE = "Required fields missing, please provide them with the following pattern: \n" \
    + "    {pattern}\n" \
    + "e.g. '{example}'\n" \
    + "or to start over: '{start_over}'\n"

INPUT_GUIDE_OPTIONAL_PARAM_TEMPLAGE = "How would you like to handle the optional filed [{optional_field}]? \n" \
    + "    - ADD {optional_field_upper}: '{field_pattern}'\n" \
    + "    - SKIP {optional_field_upper}: '{skip_it}'\n" \
    + "    - SKIP ALL: '{skip_all}'\n" \
    + "    - START OVER: '{start_over}'\n"


def get_inputguide_required_params(
        min_complete_pattern_readable: str,
        example: str,
        start_over_pattern_readable: str
):
    """
    returns the input guide that help user to provide all required params that match the min_complete_pattern

    Args:
        min_complete_pattern_readable(str): the min_complete_pattern in a human readable format
        example(str): an example input that matches the min_complete_pattern
        start_over_pattern_readable(str): the command to start over the entire input process

    Returns:
        well formated input guide based on the above INPUT_GUIDE_REQUIRED_TEMPLATE
    """
    return INPUT_GUIDE_REQUIRED_PARAMS_TEMPLATE.format(
        pattern=min_complete_pattern_readable,
        example=example,
        start_over=start_over_pattern_readable
    )


def get_inputguide_optional_param(
        param_name: str,
        pattern_readable: str,
        skip_it_pattern_readable: str,
        skip_all_pattern_readable: str,
        start_over_pattern_readable: str
):
    """
    returns the input guide for the given optional parameter

    Args:
        param_name(str): the parameter's name
        pattern_readable(str): the parameter's pattern in a human readable format
        skip_it_pattern_readable(str): the command to skip current field
        skip_all_pattern_readable(str): the command to skip all optional fields

    Returns:
        well formated input guide based on the above INPUT_GUIDE_OPTIONAL_TEMPLAGE
    """
    return INPUT_GUIDE_OPTIONAL_PARAM_TEMPLAGE.format(
        optional_field=param_name,
        optional_field_upper=param_name.upper(),
        field_pattern=pattern_readable,
        skip_it=skip_it_pattern_readable,
        skip_all=skip_all_pattern_readable,
        start_over=start_over_pattern_readable
    )
