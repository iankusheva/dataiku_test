import unittest
import requests
from framework.utils import requests_utils, logging_helpers


log = logging_helpers.set_log()


class TestTokenAuth(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    @unittest.skip
    def test_adding_task_with_a_valid_tag(self):
        # :(
        log.info("Step 1. Get authentication token")
        token_info = self.api_helpers.authenticate({"username": self.username, "password": self.password}).json()
        token = token_info.get("token")

        headers = {'Authorization': 'Bearer ' + token}
        rsp = requests.put('http://iankusheva.qatest.dataiku.com/', data={"title": "title0"}, headers=headers)
        assert rsp.status_code == 200





