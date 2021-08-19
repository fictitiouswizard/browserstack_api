import unittest

from .app_automate.appium.devices import TestDevicesApi
from .app_automate.appium.plans import TestPlansApi
from .app_automate.appium.apps import apps_api_test_suite
from .app_automate.appium.builds import builds_api_test_suite
from .app_automate.appium.projects import projects_api_test_suite
from .app_automate.appium.sessions import sessions_api_test_suite


def main():
    runner = unittest.TextTestRunner(verbosity=2)

    runner.run(unittest.makeSuite(TestDevicesApi))
    runner.run(unittest.makeSuite(TestPlansApi))
    runner.run(apps_api_test_suite())
    runner.run(builds_api_test_suite())
    runner.run(projects_api_test_suite())
    runner.run(sessions_api_test_suite())


if __name__ == "__main__":
    main()