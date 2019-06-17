from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

TIMEOUT = 3


class SeleniumDriver:
    def get_element(self, condition, timeout=TIMEOUT):
        try:
            return WebDriverWait(self, timeout).until(condition())
        except (NoSuchElementException, WebDriverException, TimeoutException):
            return None

    def get_visible_element(self, locator, timeout=TIMEOUT):
        return self.get_element(lambda: expected_conditions.visibility_of_element_located(locator), timeout)

    def get_visible_elements(self, locator, timeout=TIMEOUT):
        return self.get_element(lambda: expected_conditions.visibility_of_all_elements_located(locator), timeout)

    def get_visible_elem_by_id(self, elem_id, timeout=TIMEOUT):
        return self.get_visible_element((By.ID, elem_id), timeout)

    def get_visible_elems_by_id(self, elem_id, timeout=TIMEOUT):
        return self.get_visible_elements((By.ID, elem_id), timeout)

    def get_visible_elem_by_xpath(self, xpath, timeout=TIMEOUT):
        return self.get_visible_element((By.XPATH, xpath), timeout)

    def get_visible_elem_by_name(self, name, timeout=TIMEOUT):
        return self.get_visible_element((By.NAME, name), timeout)

    def get_visible_elems_by_xpath(self, xpath, timeout=TIMEOUT):
        return self.get_visible_elements((By.XPATH, xpath), timeout)


class SeleniumChrome(SeleniumDriver, webdriver.Chrome):
    pass


class SeleniumFirefox(SeleniumDriver, webdriver.Firefox):
    pass