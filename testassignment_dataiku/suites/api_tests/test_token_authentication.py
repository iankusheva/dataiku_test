import unittest
import base64
import uuid
import datetime
import time

from framework.utils import requests_utils, logging_helpers, data_checker


log = logging_helpers.set_log()


class TestTokenAuth(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.title = "test_title"
        self.valid_tag = str(uuid.uuid4())[:20]

        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_adding_task_with_auth(self):
        log.info("Step 1. Get authentication token")
        _, token = self.get_token(self.username, self.password)

        log.info("Step 2. Create a new task using token for authorization")
        headers = self.api_helpers.create_auth_headers(token)
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        self.api_helpers.create_task_with_token(params, headers=headers)

        log.info("Step 3. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=self.title, tags=[self.valid_tag], username=self.username)

    def test_adding_task_with_auth_incorrect_token(self):
        log.info("Step 1. Get authentication token")
        token_info, _ = self.get_token(self.username, self.password)
        token = token_info.get("token") + "extra"
        token = "{}:".format(token)  # username:password
        encoded_token = base64.b64encode(token.encode()).decode()

        log.info("Step 2. Create a new task using a different token for authorization")
        headers = self.api_helpers.create_auth_headers(encoded_token)
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        rsp = self.api_helpers.create_task_with_token(params, headers=headers, verify=False)
        assert rsp.status_code == 401, "Tasks should not be created without proper authentication"

        log.info("Step 3. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 0, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

    def test_auth_nonexistent_user(self):
        log.info("Step 1. Get authentication token")
        rsp = self.api_helpers.authenticate(self.api_helpers.create_params_for_auth("new_user", self.password), verify=False)
        assert rsp.status_code == 401, "Auth token must not be created for nonexistent users"

    @unittest.skip("Test takes 10+ minutes")
    def test_adding_task_with_auth_expired_token(self):
        log.info("Step 1. Get authentication token")

        token_creation_time = datetime.datetime.now()
        expiration_period, token = self.get_token(self.username, self.password)

        log.info("Step 2. Create a new task using token for authorization before expiration")
        time.sleep(expiration_period - 30)
        assert datetime.datetime.now() - token_creation_time < datetime.timedelta(seconds=expiration_period)
        headers = self.api_helpers.create_auth_headers(token)
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        self.api_helpers.create_task_with_token(params, headers=headers)

        log.info("Step 3. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=self.title, tags=[self.valid_tag], username=self.username)

        log.info("Step 4. Create a new task using token for authorization after expiration")
        time.sleep(40)
        assert datetime.datetime.now() - token_creation_time > datetime.timedelta(seconds=expiration_period)
        params = self.api_helpers.create_params_for_task_creation(self.title + "_new", [self.valid_tag])
        rsp = self.api_helpers.create_task_with_token(params, headers=headers, verify=False)
        assert rsp.status_code == 401, "Tasks must not be created with expired token"

        log.info("Step 5. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

    def get_token(self, username, password):
        token_info = self.api_helpers.authenticate(
            self.api_helpers.create_params_for_auth(username, password)).json()
        token = token_info.get("token")
        expiration = token_info.get("expires")
        assert token, "Couldn't obtain token from json response"
        assert expiration, "Couldn't obtain expiration period from json response"
        token = "{}:".format(token)  # username:password
        encoded_token = base64.b64encode(token.encode()).decode()
        return token_info, encoded_token



