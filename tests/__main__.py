import unittest

# from .app_automate.media import test_suite_media, test_suite_media_api
# from .app_automate.appium.devices import TestDevicesApi
# from .app_automate.appium.plans import TestPlansApi
# from .app_automate.appium.apps import apps_api_test_suite
# from .app_automate.appium.builds import builds_api_test_suite
# from .app_automate.appium.projects import projects_api_test_suite
# from .app_automate.appium.sessions import sessions_api_test_suite, session_test_suite
from .app_automate.appium import utils


def main():
    from bsapi import Settings
    Settings.bootstrap()

    runner = unittest.TextTestRunner(verbosity=2)

    test_results = [
        # runner.run(test_suite_media_api()),
        # runner.run(test_suite_media()),
        # runner.run(unittest.makeSuite(TestDevicesApi)),
        # runner.run(unittest.makeSuite(TestPlansApi)),
        # runner.run(apps_api_test_suite()),
        # runner.run(builds_api_test_suite()),
        # runner.run(projects_api_test_suite()),
        # runner.run(sessions_api_test_suite()),
        # runner.run(session_test_suite())
        runner.run(utils.connect_test_suite())
    ]

    for test_result in test_results:
        if len(test_result.errors) > 0:
            return 1
        if len(test_result.failures) > 0:
            return 2
    return 0


if __name__ == "__main__":
    exit(main())
