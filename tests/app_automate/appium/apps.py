import unittest

from bsapi.app_automate.appium import AppsApi


class TestAppsApi(unittest.TestCase):

    def test_upload_app(self):
        app = AppsApi.upload_app("./apps/ApiDemos-debug.apk", custom_id="calc")
        self.assertEqual("calc", app.custom_id)

    def test_uploaded_apps(self):
        apps = AppsApi.uploaded_apps("calc")
        self.assertGreaterEqual(len(apps), 1)

    def test_uploaded_apps_by_group(self):
        apps = AppsApi.uploaded_apps_by_group()
        self.assertGreaterEqual(len(apps), 1)

    def test_delete_app(self):
        apps = AppsApi.uploaded_apps("calc")
        response = AppsApi.delete_app(apps[0].app_id)
        self.assertEqual(True, response)


def apps_api_test_suite():
    runner = unittest.TextTestRunner(verbosity=2)

    suite = unittest.TestSuite()

    suite.addTest(TestAppsApi("test_upload_app"))
    suite.addTest(TestAppsApi("test_uploaded_apps"))
    suite.addTest(TestAppsApi("test_uploaded_apps_by_group"))
    suite.addTest(TestAppsApi("test_delete_app"))

    test_result = runner.run(suite)

    if len(test_result.errors) > 0:
        return 1
    if len(test_result.failures) > 0:
        return 2
    return 0



