import unittest
from bsapi import Settings
from .app_automate.appium import utils


def run_tests(test):
    runner = unittest.TextTestRunner(verbosity=2)

    Settings.conf_loader = utils.StaticConfig()
    Settings.bootstrap()
    Settings.get_config()

    return runner.run(test)
