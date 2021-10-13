import unittest
import os
import os.path
from concurrent import futures
import multiprocessing as mp

import tests.utils
from bsapi import Settings

from .app_automate.media import test_suite_media, test_suite_media_api
from .app_automate.appium.devices import TestDevicesApi
from .app_automate.appium.plans import TestPlansApi
from .app_automate.appium.apps import apps_api_test_suite
from .app_automate.appium.builds import builds_api_test_suite
from .app_automate.appium.projects import projects_api_test_suite
from .app_automate.appium.sessions import sessions_api_test_suite, session_test_suite
from .app_automate.appium import utils

from tests.utils import run_tests


def main():
    if os.path.isfile(os.path.join(Settings.base_dir, "bsapi.json")):
        os.remove(os.path.join(Settings.base_dir, "bsapi.json"))

    Settings.bootstrap()
    Settings.get_config()

    tests = [
        test_suite_media_api,
        test_suite_media,
        # unittest.makeSuite(TestDevicesApi),
        # unittest.makeSuite(TestPlansApi),
        apps_api_test_suite,
        builds_api_test_suite,
        projects_api_test_suite,
        sessions_api_test_suite,
        session_test_suite,
        utils.connect_test_suite,
    ]

    results = []

    with futures.ProcessPoolExecutor(max_workers=5) as pool:
        for test in tests:
            results.append(pool.submit(test))

    for test_result in futures.as_completed(results):
        print(test_result.result())
        # if len(test_result.result().errors) > 0:
        #     return 1
        # if len(test_result.result().failures) > 0:
        #     return 2

    # test_results = [
    #     runner.run(test_suite_media_api()),
    #     runner.run(test_suite_media()),
    #     runner.run(unittest.makeSuite(TestDevicesApi)),
    #     runner.run(unittest.makeSuite(TestPlansApi)),
    #     runner.run(apps_api_test_suite()),
    #     runner.run(builds_api_test_suite()),
    #     runner.run(projects_api_test_suite()),
    #     runner.run(sessions_api_test_suite()),
    #     runner.run(session_test_suite()),
    #     runner.run(utils.connect_test_suite()),
    # ]
    #
    # for test_result in test_results:
    #     if len(test_result.errors) > 0:
    #         return 1
    #     if len(test_result.failures) > 0:
    #         return 2
    return 0


if __name__ == "__main__":
    exit(main())
