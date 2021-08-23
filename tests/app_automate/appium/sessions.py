import os.path
import time
import unittest

from appium import webdriver
from requests.exceptions import HTTPError

from bsapi import Settings
from bsapi.app_automate.appium import AppsApi
from bsapi.app_automate.appium import BuildsApi
from bsapi.app_automate.appium import ProjectsApi
from bsapi.app_automate.appium import SessionsApi
from bsapi.app_automate.appium.sessions import SessionStatus, Session


def setup_session_test():
    uploaded_app = AppsApi.upload_app("./bin/ApiDemos-debug.apk", custom_id="Calc")
    app = AppsApi.uploaded_apps(uploaded_app.custom_id)[0]

    desired_caps = {
        "build": "Python Android",
        "device": "Samsung Galaxy S8 Plus",
        "app": app.app_url,
        "project": "BrowserStack Rest API",
        "browserstack.networkLogs": "true",
        "browserstack.deviceLogs": "true",
        "browserstack.appiumLogs": "true",
        "browserstack.video": "true"
    }

    url = f"https://{Settings.username}:{Settings.password}@hub-cloud.browserstack.com/wd/hub"

    driver = webdriver.Remote(url, desired_caps)
    session_id = driver.session_id
    driver.quit()

    session = Session.by_id(session_id)
    build_id = session.build.hashed_id
    project_id = session.project.project_id

    return {
        "app": app,
        "project": project_id,
        "build": build_id,
        "session": session_id
    }


def tear_down_session_test(app, project, build, session):
    try:
        AppsApi.delete_app(app.app_id)
    except HTTPError as e:
        if e.response.status_code == 422:
            apps = AppsApi.uploaded_apps()
            if len(apps) != 0:
                raise e
        else:
            raise e
    time.sleep(1)
    try:
        BuildsApi.delete(build)
    except HTTPError as e:
        if e.response.status_code == 422:
            c_build = [b for b in BuildsApi.recent_builds() if b.name == build.name]
            if len(c_build) != 0:
                BuildsApi.delete(build)
        else:
            raise e
    time.sleep(1)
    try:
        ProjectsApi.delete(project)
    except HTTPError as e:
        if e.response.status_code == 422:
            c_project = [p for p in ProjectsApi.recent_projects() if p.name == project.name]
            if len(c_project) != 0:
                ProjectsApi.delete(project)
        else:
            raise e


class TestSession(unittest.TestCase):

    app = None
    session_id = None
    build_id = None
    project_id = None

    @classmethod
    def setUpClass(cls) -> None:
        test_info = setup_session_test()
        cls.app = test_info["app"]
        cls.project_id = test_info["project"]
        cls.build_id = test_info["build"]
        cls.session_id = test_info["session"]

    @classmethod
    def tearDownClass(cls) -> None:
        tear_down_session_test(cls.app, cls.project_id, cls.build_id, cls.session_id)

    def test_session_by_id(self):
        session = Session.by_id(TestSession.session_id)
        self.assertEqual(session.hashed_id, TestSession.session_id)

    def test_build(self):
        session = Session.by_id(TestSession.session_id)
        self.assertEqual(session.build.name, "Python Android")

    def test_project(self):
        session = Session.by_id(TestSession.session_id)
        self.assertEqual(session.project.name, "BrowserStack Rest API")

    def test_get_session_logs(self):
        session = Session.by_id(TestSession.session_id)
        with session.get_session_logs() as response:
            self.assertGreater(len(response.content), 0)

    def test_get_appium_logs(self):
        session = Session.by_id(TestSession.session_id)
        with session.get_appium_logs() as response:
            self.assertGreater(len(response.content), 0)

    def test_get_device_logs(self):
        session = Session.by_id(TestSession.session_id)
        with session.get_device_logs() as response:
            self.assertGreater(len(response.content), 0)

    def test_get_network_logs(self):
        session = Session.by_id(TestSession.session_id)
        with session.get_network_logs() as response:
            self.assertGreater(len(response.content), 0)

    def test_get_video(self):
        session = Session.by_id(TestSession.session_id)
        with session.get_video() as response:
            self.assertGreater(len(response.content), 0)

    def test_save_session_logs(self):
        session = Session.by_id(TestSession.session_id)
        session.save_session_logs("./session.log")
        if os.path.isfile("./session.log"):
            os.remove("./session.log")
            self.assertTrue(True)
        else:
            self.fail()

    def test_save_appium_logs(self):
        session = Session.by_id(TestSession.session_id)
        session.save_appium_logs("./appium.log")
        if os.path.isfile("./appium.log"):
            os.remove("./appium.log")
            self.assertTrue(True)
        else:
            self.fail()

    def test_save_device_logs(self):
        session = Session.by_id(TestSession.session_id)
        session.save_device_logs("./device.log")
        if os.path.isfile("./device.log"):
            os.remove("./device.log")
            self.assertTrue(True)
        else:
            self.fail()

    def test_save_network_logs(self):
        session = Session.by_id(TestSession.session_id)
        session.save_network_logs("./network.log")
        if os.path.isfile("./network.log"):
            os.remove("./network.log")
            self.assertTrue(True)
        else:
            self.fail()

    def test_save_video(self):
        session = Session.by_id(TestSession.session_id)
        session.save_video("./session.mp4")
        if os.path.isfile("./session.mp4"):
            os.remove("./session.mp4")
            self.assertTrue(True)
        else:
            self.fail()


class TestSessionsApi(unittest.TestCase):

    app = None
    project_id = None
    build_id = None
    session_id = None

    @classmethod
    def setUpClass(cls) -> None:
        test_info = setup_session_test()
        cls.app = test_info["app"]
        cls.project_id = test_info["project"]
        cls.build_id = test_info["build"]
        cls.session_id = test_info["session"]

    @classmethod
    def tearDownClass(cls) -> None:
        tear_down_session_test(cls.app, cls.project_id, cls.build_id, cls.session_id)

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


def session_test_suite():
    suite = unittest.TestSuite()

    suite.addTest(TestSession("test_session_by_id"))
    suite.addTest(TestSession("test_build"))
    suite.addTest(TestSession("test_project"))
    suite.addTest(TestSession("test_get_session_logs"))
    suite.addTest(TestSession("test_get_appium_logs"))
    suite.addTest(TestSession("test_get_device_logs"))
    suite.addTest(TestSession("test_get_network_logs"))
    suite.addTest(TestSession("test_get_video"))
    suite.addTest(TestSession("test_save_session_logs"))
    suite.addTest(TestSession("test_save_appium_logs"))
    suite.addTest(TestSession("test_save_device_logs"))
    suite.addTest(TestSession("test_save_network_logs"))
    suite.addTest(TestSession("test_save_video"))

    return suite


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
