from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Common:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://iankusheva.qatest.dataiku.com/web/index.html"
        self.driver.get(self.url)


class MainPage(Common):
    @property
    def delete_task_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click: $parent.remove')]")

    @property
    def mark_in_progress_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click: $parent.markInProgress')]")

    @property
    def mark_done_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click: $parent.markDone')]")

    @property
    def task_text_field(self):
        return self.driver.get_visible_elem_by_xpath("//b[contains(@data-bind, 'text: title')]").text

    @property
    def owner_text_field(self):
        return self.driver.get_visible_elem_by_xpath("//b[contains(@data-bind, 'text: username')]").text

    @property
    def tags_text_elements(self):
        return self.driver.get_visible_elems_by_xpath("//span[contains(@data-bind, 'text: tag.name')]")

    @property
    def tasks_table_rows(self):
        table = self.driver.get_visible_elems_by_xpath("//table[contains(@class, 'table table-striped')]")[0]
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        return rows

    @property
    def tags_text_field(self):
        tags_elems = self.tags_text_elements
        tags_text = [tag.text for tag in tags_elems]
        return tags_text

    @property
    def date_text_field(self):
        return self.driver.get_visible_elem_by_xpath("//span[contains(@data-bind, 'text: date')]").text

    @property
    def done_status(self):
        return True if self.driver.get_visible_elem_by_xpath("//span[contains(@class, 'label label-')]") else False

    @property
    def sign_out_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click: logout')]")

    def delete_task(self):
        self.delete_task_button.click()

    def mark_in_progress(self):
        self.mark_in_progress_button.click()

    def mark_done(self):
        self.mark_done_button.click()

    def logout(self):
        self.sign_out_button.click()

    def get_task_info(self):
        return {"title": self.task_text_field, "username": self.owner_text_field, "tags": self.tags_text_field,
                "date": self.date_text_field, "done": self.done_status}


class Login(Common):

    @property
    def username_field(self):
        return self.driver.get_visible_elem_by_name("username")

    @property
    def password_field(self):
        return self.driver.get_visible_elem_by_name("password")

    def login(self, username, password):
        self.username_field.clear()
        self.username_field.send_keys(username)

        self.password_field.clear()
        self.password_field.send_keys(password)
        self.password_field.send_keys(Keys.RETURN)


class AddTask(Common):

    @property
    def title_field(self):
        return self.driver.get_visible_elem_by_xpath("//input[contains(@data-bind, 'value: title')]")

    @property
    def tags_field(self):
        return self.driver.get_visible_elem_by_xpath("//input[contains(@data-bind, 'value: tags')]")

    @property
    def add_task_confirm_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click:addTask')]")

    @property
    def add_task_button(self):
        return self.driver.get_visible_elem_by_id("btn-add")

    def add_task(self, title, tags):
        self.add_task_button.click()
        self.title_field.clear()
        self.tags_field.clear()
        self.title_field.send_keys(title)
        self.tags_field.send_keys(tags)
        self.add_task_confirm_button.click()


class EditTask(Common):

    @property
    def task_text_field_edit(self):
        return self.driver.get_visible_elem_by_xpath("//input[contains(@data-bind, 'value: title')]")

    @property
    def tags_text_elements_edit(self):
        return self.driver.get_visible_elems_by_id("inputTags")

    @property
    def mark_done_checkbox(self):
        return self.driver.get_visible_elem_by_xpath("//input[contains(@data-bind, 'checked: done')]")

    @property
    def edit_task_confirm_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click:editTask')]")

    @property
    def edit_task_button(self):
        return self.driver.get_visible_elem_by_xpath("//button[contains(@data-bind, 'click: $parent.beginEdit')]")

    def edit_task(self, title=None, tags=None, done=None):
        self.edit_task_button.click()
        if title:
            self.task_text_field_edit.click()
            self.task_text_field_edit.clear()
            self.task_text_field_edit.send_keys(title)
        if tags:
            existing_tags = self.tags_text_elements_edit
            if len(tags) < len(existing_tags):
                for elem in existing_tags:
                    elem.clear()
                for elem, text in zip(existing_tags, tags):
                    elem.send_keys(text)
        if done is not None:
            self.mark_done_checkbox.click()
        self.edit_task_confirm_button.click()


class TodoPage(MainPage, AddTask, EditTask, Login):

    def __init__(self, driver):
        super(TodoPage, self).__init__(driver)
