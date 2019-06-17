import unittest
import uuid
from framework.utils import requests_utils, logging_helpers


log = logging_helpers.set_log()


class TestTagsList(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_adding_task_with_a_valid_tag(self):
        tag = str(uuid.uuid4())[:20]
        title = "test_title"

        log.info("Step 1. Create a new task with a valid tag")
        params = self.api_helpers.create_params_for_task_creation(title, [tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Check tag was saved")
        tags = self.api_helpers.get_list_of_tags().json()
        assert len(tags) == 1, "Incorrect amount of tags in db, expected {}, got {}".format(1, len(tags))
        assert list(tags.keys())[0] == tag, "Incorrect tag saved to db"

    def test_adding_task_with_duplicate_valid_tags(self):
        tag = str(uuid.uuid4())[:20]
        title = "test_title"

        log.info("Step 1. Create a new task with duplicate tags")
        params = self.api_helpers.create_params_for_task_creation(title, [tag, tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Check tag was saved")
        tags = self.api_helpers.get_list_of_tags().json()
        assert len(tags) == 1, "Incorrect amount of tags in db, expected {}, got {}".format(1, len(tags))
        assert list(tags.keys())[0] == tag, "Incorrect tag saved to db"

        log.info("Step 3. Add a new task with a new and an old duplicate tags")
        new_tag = str(uuid.uuid4())[:20]
        params = self.api_helpers.create_params_for_task_creation(title + "_new", [new_tag, tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 4. Check there is no duplicate tags in db")
        tags = self.api_helpers.get_list_of_tags().json()
        assert len(tags) == 2, "Incorrect amount of tags in db, expected {}, got {}".format(1, len(tags))
        assert sorted(list(tags.keys())) == sorted([new_tag, tag]), "Incorrect tags saved to db"

    def test_adding_task_with_no_tags(self):
        title = "test_title"

        log.info("Step 1. Create a new task with no tags")
        params = self.api_helpers.create_params_for_task_creation(title)
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Check no tags written to db")
        tags = self.api_helpers.get_list_of_tags().json()
        assert not tags, "No tags should be present in db"

    def test_adding_task_with_invalid_too_long_tag(self):
        tag = str(uuid.uuid4())[:21]
        title = "test_title"

        log.info("Step 1. Create a new task with invalid too long tag")
        params = self.api_helpers.create_params_for_task_creation(title, [tag])
        rsp = self.api_helpers.create_task(params, username=self.username, password=self.password, verify=False)
        assert rsp.status_code != 200, "Task with incorrect tags should not be saved"

        log.info("Step 2. Check to tasks were saved to db")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "Task with incorrect tags should not be saved"
        tags = self.api_helpers.get_list_of_tags().json()
        assert not tags, "No tags should be present in db"

    def test_adding_task_with_empty_tag(self):
        # test should fail, it expects OK response code if no tag is provided

        # tag = str(uuid.uuid4())[:21]
        title = "test_title"

        log.info("Step 1. Create a new task with an empty tag")
        params = self.api_helpers.create_params_for_task_creation(title, [""])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Check task is saved to db")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        tags = self.api_helpers.get_list_of_tags().json()
        assert not tags, "No tags should be present in db"

    def test_adding_task_with_tag_as_string(self):
        # test should fail, it expects an error if tag is not a list

        tag = str(uuid.uuid4())[:20]
        title = "test_title"

        log.info("Step 1. Create a new task with tag as a string, not a list of strings")
        params = self.api_helpers.create_params_for_task_creation(title, tag)
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Task with incorrect tags should not be saved"
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "Task with incorrect tags should not be saved"
        tags = self.api_helpers.get_list_of_tags().json()
        assert not tags, "No tags should be present in db"

