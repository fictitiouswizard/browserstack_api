"""
Provides wrapper classes for interacting with the the BrowserStack REST api

Exports:
    Settings
    Api

Modules:
    app_automate.appium
"""
__version__ = "0.1.0"

from bsapi.base import Api
from bsapi.configuration import BSAPIConf, ConfigLoader, Settings

from bsapi.app_automate.appium.utils import AppiumJsonLoader

Settings.conf_loader = AppiumJsonLoader
