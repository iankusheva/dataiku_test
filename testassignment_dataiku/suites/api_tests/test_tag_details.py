import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers


log = logging_helpers.set_log()


class TestTagDetails(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_add_and_update_tags(self):
        first_tag = str(uuid.uuid4())[:20]
        second_tag = str(uuid.uuid4())[:20]
        first_title = "test_title1"
        second_title = "test_title2"

        log.info("Step 1. Create a new task with a valid tag")
        params = self.api_helpers.create_params_for_task_creation(first_title, [first_tag])
        task1 = self.api_helpers.create_task(params, self.username, self.password).json()
        data_checker.check_task_details(task1, title=first_title, tags=[first_tag], username=self.username)
        tag1_id = task1.get("tags")[0].get("url", None).split("/")[-1]

        log.info("Step 2. Create another new task with a new valid tag")
        params = self.api_helpers.create_params_for_task_creation(second_title, [second_tag])
        task2 = self.api_helpers.create_task(params, self.username, self.password).json()
        data_checker.check_task_details(task2, title=second_title, tags=[second_tag], username=self.username)
        tag2_id = task2.get("tags")[0].get("url", None).split("/")[-1]

        log.info("Step 3. Check both tags are written to db")
        tag1_details = self.api_helpers.get_information_about_tag(tag1_id).json()
        data_checker.check_tag_details(tag1_details, first_tag, [first_title])

        tag2_details = self.api_helpers.get_information_about_tag(tag2_id).json()
        data_checker.check_tag_details(tag2_details, second_tag, [second_title])

        log.info("Step 4. Modify the first task with its tag = tag of the second task")
        modified_fields = self.api_helpers.create_params_for_task_modification(tags=[second_tag])
        self.api_helpers.modify_task(task1.get("id"), modified_fields, self.username, self.password)

        log.info("Step 5. Check tag1 has no linked tasks")
        tag1_details = self.api_helpers.get_information_about_tag(tag1_id).json()
        data_checker.check_tag_details(tag1_details, first_tag, [])

        log.info("Step 6. Check tag2 has 2 tasks linked")
        tag2_details = self.api_helpers.get_information_about_tag(tag2_id).json()
        data_checker.check_tag_details(tag2_details, second_tag, [first_title, second_title])


