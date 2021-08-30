import unittest

from bsapi.app_automate.appium.utils import connect, appium_test_suite
from bsapi.app_automate.appium import AppsApi
from bsapi import Settings

# Platform: android
# Package: io.appium.android.apis
# Version: 3.3.1


class ConnectTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        bs_apps = AppsApi.uploaded_apps()
        for bs_app in bs_apps:
            AppsApi.delete_app(bs_app.app_id)

    def test_connect_app_url(self):
        try:
            apps_dir = Settings.apps_dir
            app = AppsApi.upload_app(f"{apps_dir}/ApiDemos-debug.apk")
            driver = connect(caps="Example", app_url=app.app_url)
            driver.quit()
            bs_apps = AppsApi.uploaded_apps()
            for bs_app in bs_apps:
                AppsApi.delete_app(bs_app.app_id)
        except Exception as e:
            self.fail(e)
        self.assertTrue(True)

    def test_connect_app_desc(self):
        try:
            driver = connect(platform="android", package="io.appium.android.apis", version="3.3.1", caps="Example")
            driver.quit()

        except Exception as e:
            self.fail(e)
        self.assertTrue(True)


def connect_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(ConnectTestCase("test_connect_app_url"))
    suite.addTest(ConnectTestCase("test_connect_app_desc"))
    suite.addTest(ConnectTestCase("test_connect_app_desc"))

    return suite
