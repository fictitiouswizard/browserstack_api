import unittest

from appium import webdriver

from bsapi import Settings
from bsapi.app_automate.appium import AppsApi
from bsapi.app_automate.appium import BuildsApi
from bsapi.app_automate.appium import ProjectsApi
from bsapi.app_automate.appium import SessionsApi
from bsapi.app_automate.appium.sessions import SessionStatus


class TestSessionsApi(unittest.TestCase):

    app = None
    build_id = None
    session_id = None

    @classmethod
    def setUpClass(cls) -> None:
        uploaded_app = AppsApi.upload_app("./bin/Calculator.apk", custom_id="Calc")
        app = AppsApi.uploaded_apps(uploaded_app.custom_id)[0]
        cls.app = app

        desired_caps = {
            "build": "Python Android",
            "device": "Samsung Galaxy S8 Plus",
            "app": app.app_url,
            "project": "BrowserStack Rest API",
            "browserstack.networkLogs": "true"
        }

        url = f"https://{Settings.username}:{Settings.password}@hub-cloud.browserstack.com/wd/hub"

        driver = webdriver.Remote(url, desired_caps)
        cls.session_id = driver.session_id
        driver.quit()

        builds = BuildsApi.recent_builds()
        cls.build_id = [b.hashed_id for b in builds if b.name == "Python Android"][0]

    @classmethod
    def tearDownClass(cls) -> None:
        AppsApi.delete_app(cls.app.app_id)
        builds = BuildsApi.recent_builds()
        for build in builds:
            BuildsApi.delete(build.hashed_id)
        projects = ProjectsApi.recent_projects()
        for project in projects:
            ProjectsApi.delete(project.project_id)

    def test_session_details(self):
        session = SessionsApi.details(TestSessionsApi.session_id)
        self.assertGreaterEqual(len(session.hashed_id), 1)

    def test_update_status(self):
        session = SessionsApi.update_status(TestSessionsApi.session_id, SessionStatus.failed, "Because")
        self.assertEqual(session.status, SessionStatus.failed)

    def test_delete(self):
        response = SessionsApi.delete(TestSessionsApi.session_id)
        self.assertEqual(response.status, "ok")

    def test_get_text_logs(self):
        with SessionsApi.get_text_logs(TestSessionsApi.build_id, TestSessionsApi.session_id) as response:
            self.assertGreater(len(response.content), 0)

    def test_get_appium_logs(self):
        with SessionsApi.get_appium_logs(TestSessionsApi.build_id, TestSessionsApi.session_id) as response:
            self.assertGreater(len(response.content), 0)

    def test_get_device_logs(self):
        build_id = TestSessionsApi.build_id
        session_id = TestSessionsApi.session_id
        with SessionsApi.get_device_logs(build_id, session_id) as response:
            self.assertGreater(len(response.content), 0)

    def test_get_network_logs(self):
        build_id = TestSessionsApi.build_id
        session_id = TestSessionsApi.session_id
        with SessionsApi.get_network_logs(build_id, session_id) as response:
            self.assertGreater(len(response.content), 0)

    def test_get_profiling_data(self):
        build_id = TestSessionsApi.build_id
        session_id = TestSessionsApi.session_id
        profiling_data = SessionsApi.get_profiling_data(build_id, session_id)
        self.assertGreater(len(profiling_data), 0)


def sessions_api_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(TestSessionsApi("test_session_details"))
    suite.addTest(TestSessionsApi("test_update_status"))
    suite.addTest(TestSessionsApi("test_get_text_logs"))
    suite.addTest(TestSessionsApi("test_get_appium_logs"))
    suite.addTest(TestSessionsApi("test_get_device_logs"))
    suite.addTest(TestSessionsApi("test_get_network_logs"))
    suite.addTest(TestSessionsApi("test_get_profiling_data"))
    suite.addTest(TestSessionsApi("test_delete"))

    return suite
