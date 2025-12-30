import pathlib
import tempfile
import base64

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
ANDROID_VERSION = '16.0'
DEVICE_NAME = 'emulator-5554'


@pytest.fixture(scope="session")
def appium_service():
    service = AppiumService()
    service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)], timeout_ms=20 * 1000)
    yield service
    service.stop()


def get_android_driver(custom_options=None):
    options = UiAutomator2Options()
    options.platform_version = ANDROID_VERSION
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


def test_record_video(appium_service, android_driver_factory):
    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': DEVICE_NAME}
    with android_driver_factory(custom_opts) as driver:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = pathlib.Path(temp_dir) / 'alert_dialogs_video.mp4'
            options = {
                'timeLimit': '300',  # seconds
                'videoType': 'mp4',
            }
            driver.start_recording_screen(options=options)

            elem = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("App")')
            elem.click()

            elem = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Alert Dialogs")')
            elem.click()

            video = driver.stop_recording_screen()
            # stop_recording_screen returns base64-encoded video (str) in many drivers;
            # decode it before writing to disk so the mp4 file is valid.
            if isinstance(video, str):
                data = base64.b64decode(video)
            else:
                data = video

            with open(video_path, 'wb') as f:
                f.write(data)

            print(f'Video path: {video_path}')
            assert video_path.is_file()
