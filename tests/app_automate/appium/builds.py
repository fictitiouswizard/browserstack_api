import unittest

from appium import webdriver
from requests.exceptions import HTTPError

from bsapi.app_automate.appium import BuildsApi
from bsapi.app_automate.appium import AppsApi
from bsapi import Settings


class TestBuildsApi(unittest.TestCase):

    app = None

    @classmethod
    def setUpClass(cls) -> None:
        uploaded_app = AppsApi.upload_app("./bin/ApiDemos-debug.apk", custom_id="Calc")
        app = AppsApi.uploaded_apps(uploaded_app.custom_id)[0]
        cls.app = app

        desired_caps = {
            "build": "Python Android",
            "device": "Samsung Galaxy S8 Plus",
            "app": app.app_url,
            "project": "BrowserStack Rest API"
        }

        url = f"https://{Settings.username}:{Settings.password}@hub-cloud.browserstack.com/wd/hub"
        driver = webdriver.Remote(url, desired_caps)
        driver.quit()

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            AppsApi.delete_app(cls.app.app_id)
        except HTTPError as e:
            if e.response.status_code == 422:
                apps = AppsApi.uploaded_apps()
                if len(apps) != 0:
                    raise e
            else:
                raise e

    def test_recent_builds(self):
        builds = BuildsApi.recent_builds()
        self.assertGreaterEqual(len(builds), 1)

    def test_details(self):
        builds = BuildsApi.recent_builds()
        sessions = BuildsApi.details(builds[0].hashed_id)
        self.assertGreaterEqual(len(sessions), 1)

    def test_delete(self):
        builds = BuildsApi.recent_builds()
        response = BuildsApi.delete(builds[0].hashed_id)
        self.assertEqual(response.status, "ok")


def builds_api_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(TestBuildsApi("test_recent_builds"))
    suite.addTest(TestBuildsApi("test_details"))
    suite.addTest(TestBuildsApi("test_delete"))

    return suite
