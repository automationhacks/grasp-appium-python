from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def tap(self, AppiumBy, locator, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((AppiumBy, locator)))
        elem.click()

    def find_element(self, AppiumBy, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((AppiumBy, locator)))
