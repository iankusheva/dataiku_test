import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers


log = logging_helpers.set_log()


class TestUserCreation(unittest.TestCase):
    def setUp(self):
        self.default_username = "QA"
        self.default_password = "willWin"
        self.new_username = "new_user"
        self.new_password = "new_pass!@_(DSF*&fksdjh%^^#kjhdfglfdlh1232138&&*7dsflk459(((9dsfw&&*"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_create_new_user_valid_fields(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title1"

        log.info("Step 1. Create new user")
        self.api_helpers.create_new_user({"username": self.new_username, "password": self.new_password})

        log.info("Step 2. Create new valid task with new user")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        task1 = self.api_helpers.create_task(params, self.new_username, self.new_password).json()
        data_checker.check_task_details(task1, title=test_title, tags=[test_tag], username=self.new_username)

    def test_new_user_with_duplicate_username(self):
        log.info("Step 1. Create new user with username being equal to default username")
        rsp = self.api_helpers.create_new_user({"username": self.default_username, "password": self.new_password}, verify=False)
        assert rsp.status_code != 200, "Changing password of existing user is not permitted"

    def test_new_user_with_duplicate_password(self):
        # test should fail, it expects OK response code if there is any other user saved with the same pass

        log.info("Step 1. Create new user with password being equal to default password")
        rsp = self.api_helpers.create_new_user({"username": self.new_username, "password": self.default_password}, verify=False)
        assert rsp.status_code == 200, "Couldn't create new user with duplicate password"




