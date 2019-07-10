"""
    Collection of Jira API related util functions
"""
import re


def format_issue_key(issue_key_str: str):
    """
    returns formatted issueKey according to <CAPTIAL_LETTERS>-<NUMBERS>
    with capital letters, dash, numbers, no spaces

    Args:
        issue_key_str(str): issue key that caught by RE

    Returns:
        issue_key(str): formatted issue_key

    """

    issue_key_str = issue_key_str.upper().replace(' ', '')

    issue_prefix = ''.join([c for c in issue_key_str if c.isalpha()])
    issue_number = ''.join([c for c in issue_key_str if c.isdigit()])

    issue_key = '{}-{}'.format(issue_prefix, issue_number)

    return issue_key


def format_time_spent(time_spent_str: str):
    """
    returns formatted time_spent in seconds

    Args:
        time_spent_str: time spent that caught by RE

    Returns:
        time_spent(str): formatted time spent in seconds

    """

    scales = {
        'day': 28800,   # 8 * 3600
        'hour': 3600,
        'hours': 3600,
        'minute': 60,
        'minutes': 60,
    }

    num = float(re.search(r'\d+(\.\d+)?', time_spent_str).group())
    scale = re.sub(r'[^a-zA-Z]', '', time_spent_str)
    scale_in_seconds = scales.get(scale)
    if not scale_in_seconds or not num:
        message = "[timeSpent process error] failed to convert timeSpent '{}' into seconds" \
            .format(time_spent_str)
        raise Exception(message)

    time_spent_seconds = num * scale_in_seconds

    return int(time_spent_seconds)
