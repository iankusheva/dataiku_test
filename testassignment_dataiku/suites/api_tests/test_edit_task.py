import unittest
import uuid
from framework.utils import requests_utils, data_checker, logging_helpers


log = logging_helpers.set_log()


class TestTaskEditing(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_edit_task_with_valid_fields(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to edit")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Modify the task")
        new_title = "new_test_title"
        new_tag = str(uuid.uuid4())[:20]
        done = True
        modified_fields = self.api_helpers.create_params_for_task_modification(title=new_title, tags=[new_tag], done=done)
        self.api_helpers.modify_task(task_id, modified_fields, self.username, self.password)

        log.info("Step 4. Check the task is modified correctly")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=new_title, tags=[new_tag], username=self.username, done=done)

    def test_modify_task_without_auth(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to modify")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Modify task with valid fields without authentication")
        new_title = "new_test_title"
        new_tag = str(uuid.uuid4())[:20]
        done = True
        modified_fields = self.api_helpers.create_params_for_task_modification(title=new_title, tags=[new_tag], done=done)
        rsp = self.api_helpers.modify_task(task_id, modified_fields, self.username, self.password, needs_auth=False, verify=False)
        assert rsp.status_code != 200, "Task should not be modified without authentication"

        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=test_title, tags=[test_tag], username=self.username)

    def test_modify_existing_task_with_different_user(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title_"

        log.info("Step 1. Create a new task with valid fields, default user")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to modify")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Create new user")
        new_username = "new_user"
        new_pass = "wowmuchsecure"
        self.api_helpers.create_new_user({"username": new_username, "password": new_pass})

        log.info("Step 4. Modify task with a wrong user")
        new_title = "new_test_title"
        new_tag = str(uuid.uuid4())[:20]
        done = True
        modified_fields = self.api_helpers.create_params_for_task_modification(title=new_title, tags=[new_tag], done=done)
        rsp = self.api_helpers.modify_task(task_id, modified_fields, new_username, new_pass,
                                           verify=False)
        assert rsp.status_code != 200, "Task should not be modified if provided user is not the owner"

        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=test_title, tags=[test_tag], username=self.username)

    def test_modify_non_existent_task(self):
        log.info("Step 1. Modify non-existent task")
        new_title = "new_test_title"
        new_tag = str(uuid.uuid4())[:20]
        done = True
        modified_fields = self.api_helpers.create_params_for_task_modification(title=new_title, tags=[new_tag], done=done)
        rsp = self.api_helpers.modify_task("123312", modified_fields, self.username, self.password,
                                           verify=False)
        assert rsp.status_code != 200, "Modified non existent task"
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "There should be no tasks in db"

    def test_modify_task_immutable_fields(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to modify")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Modify immutable fields of a task")
        new_title = "new_test_title"
        new_tag = str(uuid.uuid4())[:20]
        done = "false"
        modified_fields = self.api_helpers.create_params_for_task_modification(title=new_title, tags=[new_tag], done=done, date="2018-03-14T14:43:34.009884Z", username="new_author", id=500)
        self.api_helpers.modify_task(task_id, modified_fields, self.username, self.password)

        log.info("Step 4. Check that only mutable fields were modified")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        data_checker.check_task_details(tasks[0], title=new_title, tags=[new_tag], username=self.username, done=done)
