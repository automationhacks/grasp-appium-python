import base64
import os
import tempfile
import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options

capabilities = {
    "platformName": "android",
    "appium:automationName": "uiautomator2",
    "appium:platformVersion": "16",
    "appium:deviceName": "emulator-5554",
    "appium:app": "/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk",
    "appium:appPackage": "io.appium.android.apis",
    "appium:appActivity": "io.appium.android.apis.ApiDemos"
}

appium_server_url = 'http://localhost:4723'


class PushPullFileTest(unittest.TestCase):
    """
    Test class to verify that files can be pushed to and pulled from the emulator.
    """

    def setUp(self) -> None:
        load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=load_capabilities)
        self.test_file_content = "hello to Appium Python"
        self.emulator_file_path = "/data/local/tmp/test_file.txt"
        self.local_temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        # Clean up local temporary directory
        if os.path.exists(self.local_temp_dir):
            for file in os.listdir(self.local_temp_dir):
                file_path = os.path.join(self.local_temp_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(self.local_temp_dir)

    def test_push_and_pull_file(self) -> None:
        # Step 1: Create a temporary text file with the content
        local_file_path = os.path.join(self.local_temp_dir, "test_file.txt")
        with open(local_file_path, 'w') as f:
            f.write(self.test_file_content)

        self.assertTrue(os.path.exists(local_file_path), 'Local test file was not created')

        # Step 2: Push the file to the emulator
        with open(local_file_path, 'rb') as f:
            file_data = f.read()

        encoded_file_data = base64.b64encode(file_data).decode('utf-8')
        self.driver.push_file(self.emulator_file_path, encoded_file_data)
        print(f"File pushed to emulator at {self.emulator_file_path}")

        # Step 3: Pull the file back from the emulator
        pulled_file_data_encoded = self.driver.pull_file(self.emulator_file_path)
        print(f"File pulled from emulator: {self.emulator_file_path}")

        # Step 4: Decode the pulled file data (it's base64 encoded)
        pulled_file_data = base64.b64decode(pulled_file_data_encoded)
        pulled_content = pulled_file_data.decode('utf-8')

        # Step 5: Assert that the pulled file content matches the original content
        self.assertEqual(pulled_content, self.test_file_content,
                         f'Pulled file content does not match. Expected: {self.test_file_content}, Got: {pulled_content}')

        # Step 6: Save the pulled file locally and verify it
        pulled_file_path = os.path.join(self.local_temp_dir, "pulled_test_file.txt")
        with open(pulled_file_path, 'wb') as f:
            f.write(pulled_file_data)

        self.assertTrue(os.path.exists(pulled_file_path), 'Pulled file was not saved locally')

        with open(pulled_file_path, 'r') as f:
            pulled_local_content = f.read()

        self.assertEqual(pulled_local_content, self.test_file_content,
                         'Pulled file content does not match original content')


if __name__ == '__main__':
    unittest.main()
