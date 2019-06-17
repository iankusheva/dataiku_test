import unittest

from framework.web_driver import selenium_driver
from framework.utils import requests_utils, data_checker, logging_helpers
from framework.forms import todopage


log = logging_helpers.set_log()


class TestTaskDetails(unittest.TestCase):
    def setUp(self):
        self.username = "QA"
        self.password = "willWin"
        self.title = "Test title"
        self.tags = ["tag1", "tag2", "moretags"]
        
        self.api_helpers = requests_utils.AvailableAPIActions
        self.api_helpers.reset_db()
        # fix the path!
        # self.driver = selenium_driver.SeleniumChrome(executable_path='../../chromedriver')
        self.driver = selenium_driver.SeleniumChrome()
        self.webpage = todopage.TodoPage(self.driver)
        self.needs_logout = True

    def tearDown(self) -> None:
        if self.needs_logout:
            self.webpage.logout()
        self.driver.quit()

    def test_add_task(self):
        log.info("Step 1. Login with default credentials")
        self.webpage.login(self.username, self.password)

        log.info("Step 2. Add a new task")
        self.webpage.add_task(self.title, " ".join(self.tags))

        log.info("Step 3. Check task data is present on the web page")
        task_data_from_ui = self.webpage.get_task_info()
        data_checker.check_task_details(task_data_from_ui, self.title, self.tags, self.username, False)

    def test_edit_task(self):
        # test should fail, because tags are reset after page refresh

        log.info("Step 1. Login with default credentials")
        self.webpage.login(self.username, self.password)

        log.info("Step 2. Add a new task")
        self.webpage.add_task(self.title, " ".join(self.tags))

        log.info("Step 3. Edit tags and success status of the created task")
        self.tags = ["tag0"]
        self.webpage.edit_task(tags=self.tags, done=True)

        log.info("Step 4. Check task data is present on the web page")
        self.driver.refresh()
        task_data_from_ui = self.webpage.get_task_info()
        data_checker.check_task_details(task_data_from_ui, self.title, self.tags, self.username, True)

    def test_delete_task(self):
        log.info("Step 1. Login with default credentials")
        self.webpage.login(self.username, self.password)

        log.info("Step 2. Add a new task")
        self.webpage.add_task(self.title, " ".join(self.tags))

        log.info("Step 3. Delete just created task")
        self.webpage.delete_task()
        self.driver.refresh()

        log.info("Step 4. Check task data is removed from the web page")
        tasks = self.webpage.tasks_table_rows
        assert len(tasks) == 1, "Expected no tasks, got {}".format(len(tasks) - 1)

    def test_mark_task_as_done(self):
        log.info("Step 1. Login with default credentials")
        self.webpage.login(self.username, self.password)

        log.info("Step 2. Add a new task")
        self.webpage.add_task(self.title, " ".join(self.tags))

        log.info("Step 3. Mark created task as done from main page")
        self.webpage.mark_done()

        log.info("Step 4. Check data is updated")
        task_data_from_ui = self.webpage.get_task_info()
        data_checker.check_task_details(task_data_from_ui, self.title, self.tags, self.username, True)

        log.info("Step 5. Mark created task as in progress from main page")
        self.webpage.mark_in_progress()

        log.info("Step 6. Check data is updated")
        task_data_from_ui = self.webpage.get_task_info()
        data_checker.check_task_details(task_data_from_ui, self.title, self.tags, self.username, False)

    def test_backend_data_shows_on_webpage(self):
        new_username = "new_user"
        new_password = "new_pass"

        log.info("Step 1. Create new user")
        self.api_helpers.create_new_user({"username": new_username, "password": new_password})

        log.info("Step 2. Create new valid task with new user")
        params = self.api_helpers.create_params_for_task_creation(self.title, self.tags)
        task1 = self.api_helpers.create_task(params, new_username, new_password).json()
        data_checker.check_task_details(task1, title=self.title, tags=self.tags, username=new_username)

        log.info("Step 3. Login to web page")
        self.webpage.login(new_username, new_password)
        self.driver.refresh()

        log.info("Step 4. Check task data is present on the web page")
        task_data_from_ui = self.webpage.get_task_info()
        data_checker.check_task_details(task_data_from_ui, self.title, self.tags, new_username, False)

    def test_login_incorrect_password(self):
        log.info("Step 1. Login with incorrect credentials")
        self.webpage.login(self.username, "gibberish")

        assert self.webpage.sign_out_button is None
        self.needs_logout = False
