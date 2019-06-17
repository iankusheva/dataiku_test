import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers


log = logging_helpers.set_log()


class TestTasksList(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_adding_task_with_a_valid_tag(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with a valid tag")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=test_title, tags=[test_tag], username=self.username)

    def test_adding_task_with_duplicate_valid_tags(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with duplicate tags")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag, test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Check task is written to db")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=test_title, tags=[test_tag], username=self.username)
