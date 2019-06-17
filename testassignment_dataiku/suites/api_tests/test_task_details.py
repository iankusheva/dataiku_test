import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers


log = logging_helpers.set_log()


class TestTaskDetails(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_task_details(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Check task details are correct")
        task_details = self.api_helpers.get_task_description(task_id).json()
        data_checker.check_task_details(task_details, title=test_title, tags=[test_tag], username=self.username)


