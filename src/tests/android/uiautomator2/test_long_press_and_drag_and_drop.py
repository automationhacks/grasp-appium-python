import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from assertpy import assert_that
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


@pytest.fixture(scope="session")
def appium_service():
    service = AppiumService()
    service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)], timeout_ms=20 * 1000)
    yield service
    service.stop()


def get_android_driver(custom_options=None):
    options = UiAutomator2Options()
    options.platform_version = '16.0'
    if custom_options:
        options.load_capabilities(custom_options)
    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


@pytest.fixture
def android_driver_factory():
    return get_android_driver


@pytest.fixture
def android_driver():
    driver = get_android_driver()
    yield driver
    driver.quit()


def test_get_current_activity(appium_service, android_driver_factory):
    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': 'emulator-5554'}
    with android_driver_factory(custom_opts) as driver:
        views_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Views")')
        views_button.click()

        drag_and_drop_button = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                   value='new UiSelector().text("Drag and Drop")')
        drag_and_drop_button.click()

        first_dot = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                        value='new UiSelector().resourceId("io.appium.android.apis:id/drag_dot_1")')
        second_dot = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                         value='new UiSelector().resourceId("io.appium.android.apis:id/drag_dot_2")')

        actions = ActionChains(driver)
        actions.click_and_hold(first_dot)
        actions.pause(4)
        actions.move_to_element(second_dot)
        actions.release(second_dot)
        actions.perform()

        result_label = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                                                                                         'new UiSelector().resourceId("io.appium.android.apis:id/drag_result_text")')))

        assert_that(result_label.get_attribute('text')).is_equal_to('Dropped!')
