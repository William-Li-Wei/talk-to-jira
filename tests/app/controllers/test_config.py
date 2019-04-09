import re
from app.controllers import config as conf


text = "i spent 1 day and 2.5 hours on the issue ttj-12 and then found out the issue was removed." \
    + "please update me with comment as i have no comment."


def test_number_pattern():
    expected = ['1', '2.5', '12']
    matches = re.finditer(conf.COMMON_PATTERN_NUMBER, text)
    numbers = [m.group() for m in matches]

    assert expected == numbers


def test_time_pattern():
    expected = ['day', 'hours']
    matches = re.finditer(conf.COMMON_PATTERN_TIMEUNIT, text)
    timeunits = [m.group() for m in matches]

    assert expected == timeunits


def test_timespent_pattern():
    expected = ['1 day', '2.5 hours']
    matches = re.finditer(conf.COMMON_PATTERN_TIMESPENT, text)
    timespents = [m.group() for m in matches]

    assert expected == timespents


def test_issuekey_pattern():
    expected = ['ttj-12']
    matches = re.finditer(conf.COMMON_PATTERN_ISSUEKEY, text)
    issue_keys = [m.group() for m in matches]

    assert expected == issue_keys


def test_comment_pattern():
    expected = ['i have no comment.']
    matches = re.finditer(conf.COMMON_PATTERN_COMMENT, text)
    comments = [m.group() for m in matches]

    assert expected == comments
