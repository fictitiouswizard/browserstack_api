import unittest

import bsapi.app_automate.appium as BrowserStack
from bsapi import Settings, configuration, BSAPIConf


# Platform: android
# Package: io.appium.android.apis
# Version: 3.3.1

class StaticConfig(configuration.ConfigLoader):

    @classmethod
    def bootstrap(cls, settings):
        pass

    @classmethod
    def get_app(cls, settings, plateform, package, build):
        return {
            "file_name": "ApiDemos-debug.apk",
            "package": "io.appium.android.apis",
            "version": "3.3.1",
            "build": "21",
            "platform": "android",
            "app_url": "bs://cc582ff55b916c47ba78da629da2ec23931c2dd5",
            "custom_id": "android-io.appium.android.apis-3.3.1"
        }

    @classmethod
    def save_config(cls, settings, config):
        pass

    @classmethod
    def get_config(cls, settings, config) -> BSAPIConf:
        conf = BSAPIConf()
        conf.apps = [{
            "file_name": "ApiDemos-debug.apk",
            "package": "io.appium.android.apis",
            "version": "3.3.1",
            "build": "21",
            "platform": "android",
            "app_url": "bs://cc582ff55b916c47ba78da629da2ec23931c2dd5",
            "custom_id": "android-io.appium.android.apis-3.3.1"
        }]
        conf.media = []
        conf.desired_caps = [
            {
                "dc_name": "Example",
                "name": "BSAPI Session",
                "build": "Python Android",
                "device": "Samsung Galaxy S8 Plus",
                "project": "BrowserStack Rest API",
                "browserstack.networkLogs": "true",
                "browserstack.deviceLogs": "true",
                "browserstack.appiumLogs": "true",
                "browserstack.video": "true",
                "app": "bs://64d8f602237c41d33564c85e02b8cb3b1916cf0c"
            }
        ]
        return conf


class ConnectTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        bs_apps = BrowserStack.AppsApi.uploaded_apps()
        for bs_app in bs_apps:
            BrowserStack.AppsApi.delete_app(bs_app.app_id)

    def test_connect_app_url(self):
        try:
            apps_dir = Settings.apps_dir
            app = BrowserStack.AppsApi.upload_app(f"{apps_dir}/ApiDemos-debug.apk")
            driver = BrowserStack.connect(caps="Example", app_url=app.app_url)
            driver.quit()
            bs_apps = BrowserStack.AppsApi.uploaded_apps()
            for bs_app in bs_apps:
                BrowserStack.AppsApi.delete_app(bs_app.app_id)
        except Exception as e:
            self.fail(e)
        self.assertTrue(True)

    def test_connect_app_desc(self):
        try:
            driver = BrowserStack.connect(
                platform="android", package="io.appium.android.apis", version="3.3.1", caps="Example")
            print(driver.session_id)
            driver.quit()

        except Exception as e:
            self.fail(e)
        self.assertTrue(True)


def connect_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(ConnectTestCase("test_connect_app_url"))
    suite.addTest(ConnectTestCase("test_connect_app_desc"))

    return suite
