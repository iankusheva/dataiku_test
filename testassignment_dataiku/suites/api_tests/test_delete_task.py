import unittest
import uuid
from framework.utils import requests_utils, logging_helpers


log = logging_helpers.set_log()


class TestTaskDeletion(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()

    def test_delete_existing_task(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to delete")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Delete created task")
        self.api_helpers.delete_task(task_id, self.username, self.password)
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert not tasks, "No tasks should be present in db"

    def test_delete_existing_task_wo_authentication(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to delete")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 4. Delete created task without authentication")
        rsp = self.api_helpers.delete_task(task_id, self.username, self.password, needs_auth=False, verify=False)
        assert rsp != 200, "Tasks can't be deleted without authentication"
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

    def test_delete_existing_task_with_different_user(self):
        # test should fail, it expects an error if you delete a task with a wrong user

        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title_"

        log.info("Step 1. Create a new task with valid fields, default user")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain task id to delete")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Create new user in db")
        new_username = "new_user"
        new_pass = "wowmuchsecure"
        self.api_helpers.create_new_user({"username": new_username, "password": new_pass})

        log.info("Step 4. Delete created task with a wrong user")
        rsp = self.api_helpers.delete_task(task_id, new_username, new_pass, needs_auth=True, verify=False)
        assert rsp != 200, "Tasks can't be deleted if user is not its owner"
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))

    def test_delete_non_existent_task(self):
        test_tag = str(uuid.uuid4())[:20]
        test_title = "test_title"

        log.info("Step 1. Create a new task with valid fields")
        params = self.api_helpers.create_params_for_task_creation(test_title, [test_tag])
        self.api_helpers.create_task(params, self.username, self.password)

        log.info("Step 2. Obtain created task id")
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks) == 1, "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))
        task_id = tasks[0].get("id")

        log.info("Step 3. Delete a non existent task")
        rsp = self.api_helpers.delete_task("new_".format(task_id), self.username, self.password, verify=False)
        assert rsp.status_code != 200, "Deleting non existent task should result in error"
        tasks = self.api_helpers.get_list_of_tasks().json()
        assert len(tasks), "Incorrect amount of tasks in db, expected {}, got {}".format(1, len(tasks))