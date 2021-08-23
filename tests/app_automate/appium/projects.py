import unittest

from appium import webdriver
from requests.exceptions import HTTPError

from bsapi.app_automate.appium import AppsApi
from bsapi.app_automate.appium import ProjectsApi
from bsapi.app_automate.appium import BuildsApi
from bsapi import Settings


class TestProjectsApi(unittest.TestCase):

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

    def test_recent_projects(self):
        projects = ProjectsApi.recent_projects()
        self.assertGreaterEqual(len(projects), 1)

    def test_details(self):
        projects = ProjectsApi.recent_projects()
        project = ProjectsApi.details(projects[0].project_id)
        self.assertEqual(project.name, projects[0].name)
        self.assertGreater(len(project.builds), 0)

    def test_update_project_name(self):
        projects = ProjectsApi.recent_projects()
        project = ProjectsApi.update_project_name(projects[0].project_id, "Test Rest API")
        self.assertEqual(project.name, "Test Rest API")

    def test_status_badge_key(self):
        projects = ProjectsApi.recent_projects()
        badge_key = ProjectsApi.status_badge_key(projects[0].project_id)
        self.assertGreater(len(badge_key), 0)

    def test_delete(self):
        projects = ProjectsApi.recent_projects()
        for project in projects:
            if project.builds is None:
                continue

            for build in project.builds:
                BuildsApi.delete(build.hashed_id)
            response = ProjectsApi.delete(project.project_id)
            self.assertEqual(response.status, "ok")


def projects_api_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestProjectsApi("test_recent_projects"))
    suite.addTest(TestProjectsApi("test_details"))
    suite.addTest(TestProjectsApi("test_update_project_name"))
    suite.addTest(TestProjectsApi("test_status_badge_key"))
    suite.addTest(TestProjectsApi("test_delete"))
    return suite
