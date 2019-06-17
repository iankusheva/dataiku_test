import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers

log = logging_helpers.set_log()


class TestTaskCreation(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.title = "test_title"
        self.invalid_title = str(uuid.uuid4())[:21]
        self.valid_tag = str(uuid.uuid4())[:20]
        self.invalid_tag = str(uuid.uuid4())[:21]
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_adding_task_with_valid_fields(self):
        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=self.title, tags=[self.valid_tag], username=self.username)

    def test_adding_task_without_auth(self):
        log.info("Step 1. Create a new task with valid fields without authentication")
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        rsp = self.api_helpers.create_task(params, self.username, self.password, needs_auth=False, verify=False)
        assert rsp.status_code == 401, "Tasks should not be created without authentication"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_adding_task_with_empty_title(self):
        # test should fail, it expects an error if task is created without a title

        log.info("Step 1. Create a new task with an empty title")
        params = self.api_helpers.create_params_for_task_creation("", [self.valid_tag])
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Tasks should not be created without a title"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_adding_task_with_title_too_long(self):
        # test should fail, it expects an error for tasks with titles longer than 20 symbols

        log.info("Step 1. Create a new task with invalid too long title")
        params = self.api_helpers.create_params_for_task_creation(self.invalid_title, [self.valid_tag])
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Tasks should not be created with title longer than 20 symbols"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_adding_task_with_special_symbols_in_title(self):
        # test should fail, it expects OK response code for text fields containing special symbols

        test_title = "entête de test"
        test_tag = "pas d'entête"

        log.info("Step 1. Create a new task with valid fields, title contains special symbols")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=test_title, tags=[test_tag], username=self.username)

    def test_adding_missing_fields_in_request(self):
        log.info("Step 1. Create a new task, request missing some fields")
        params = {"tags": [self.valid_tag]}
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Tasks should not be created if request is incorrect"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_adding_task_with_duplicate_title(self):
        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. There is one task in db")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

        data_checker.check_task_details(tasks[0], title=self.title, tags=[self.valid_tag], username=self.username)

        log.info("Step 3. Create a new task with valid fields, title is a duplicate")
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.valid_tag])
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Tasks should not be created with duplicate titles"

        log.info("Step 4. There is still only one task in db")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

    def test_adding_task_with_no_tags(self):
        log.info("Step 1. Create a new task with no tags")
        params = self.api_helpers.create_params_for_task_creation(self.title)
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=self.title, tags=[], username=self.username)

    def test_adding_task_with_invalid_tag_too_long(self):
        log.info("Step 1. Create a new task with invalid tag")
        params = self.api_helpers.create_params_for_task_creation(self.title, [self.invalid_tag])

        rsp = self.api_helpers.create_task(params, username=self.username, password=self.password, verify=False)
        assert rsp.status_code != 200, "Task with incorrect tags should not be saved"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_adding_task_with_empty_tag(self):
        # test should fail, it expects OK response code if no tag is provided

        log.info("Step 1. Create a new task with a valid tag")
        params = self.api_helpers.create_params_for_task_creation(self.title, [""])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain list of tasks - there is 1 task present")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=self.title, tags=[], username=self.username)

    def test_adding_task_with_invalid_format_of_tags_list(self):
        # test should fail, it expects an error or a different behavior if tags is not a list

        log.info("Step 1. Create a new task with a valid tag")
        params = self.api_helpers.create_params_for_task_creation(self.title, self.valid_tag)
        rsp = self.api_helpers.create_task(params, self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Task with incorrect tags should not be saved"

        log.info("Step 2. Obtain list of tasks - there should be none")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"
