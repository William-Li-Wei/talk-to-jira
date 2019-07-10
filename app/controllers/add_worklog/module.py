import requests

from app.controllers import util
from app.controllers.module import BaseController


class Controller(BaseController):

    url = BaseController.BASE_URL + "/rest/api/2/issue/{issueKey}/worklog"
    req_body = {}

    def prepare_url_and_req_body(self):
        """
        process the input params, compose the url and request body

        Returns:

        """
        issue_key = util.format_issue_key(self.params.get('issueKey').get('value'))
        self.url = self.url.format(issueKey=issue_key)

        time_spent_seconds = util.format_time_spent(self.params.get('timeSpent').get('value'))
        self.req_body['timeSpentSeconds'] = time_spent_seconds

        comment = self.params.get('comment').get('value')
        if comment:
            self.req_body['comment'] = comment



    def call_jira(self):
        """
        calls Jira API with the prepared URL and request body

        Returns:
            res(HTTPResponse): response of the API call

        """

        session = requests.Session()
        session.trust_env = False
        res = session.post(
            url=self.url,
            headers=self.HEADERS,
            json=self.req_body
        )

        return res
