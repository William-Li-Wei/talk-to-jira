"""
    Worklog controller
"""

from typing import Union, Optional
import requests

import config as conf


class WorklogController:
    """
    Controller for all workflow oriented actions
    """

    URL_ADD_WORKLOG = conf.DOMAIN + "/rest/api/2/issue/{issueIdOrKey}/worklog"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + conf.AUTH_HEADER
    }

    def add_worklog(self, issue_id_or_key: Union[int, str], time_spent_seconds: int, comment: Optional[str]):
        """
        Adds a new worklog entry to an issue.

        Args:
            issueIdOrKey(int or str): the issue id or key
            time_spent_seconds(int): time spent in seconds
            comment(str, optional): comment to the worklog

        Returns: response from jira
        """

        url = self.URL_ADD_WORKLOG.format(issueIdOrKey=issue_id_or_key)
        print('URL: ' + url)
        req_body = {
            "comment": comment,
            "timeSpentSeconds": time_spent_seconds
        }

        res = requests.post(
            url=url,
            headers=self.HEADERS,
            json=req_body
        )

        return res
