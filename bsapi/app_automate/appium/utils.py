import functools
import os
from os import path

from pyaxmlparser import APK
import jsonpickle
from appium import webdriver

import bsapi
from bsapi.app_automate.appium import AppsApi


class AppiumJsonLoader(bsapi.ConfigLoader):
    conf_file_name = "bsapi.json"

    @classmethod
    def get_config_file(cls, settings) -> str:
        return os.path.join(settings.base_dir, cls.conf_file_name)

    @classmethod
    def get_config(cls, settings, config) -> bsapi.configuration.BSAPIConf:
        if config is None:
            with open(cls.get_config_file(settings), "r") as config_file:
                config = jsonpickle.decode(config_file.read())
            return config
        else:
            return config

    @classmethod
    def save_config(cls, settings, config):
        with open(AppiumJsonLoader.get_config_file(settings), "w") as config_file:
            config_file.write(jsonpickle.encode(config, indent=4))

    @classmethod
    def get_app(cls, settings, platform, package, version) -> dict:
        apps = [
            app
            for app
            in settings.get_config().apps
            if app["package"] == package and app["version"] == version and app["platform"] == platform
        ]
        if len(apps) >= 1:
            print("App found")
            return apps[0]
        else:
            # Check if there are any new apps in the apps folder
            app_files = os.listdir(settings.get_apps_dir())
            app_file_names = [app["file_name"] for app in settings.get_config().apps]

            for app_file in app_files:
                if app_file in app_file_names:
                    continue
                # if new apps in the folder upload them to BS and check if any of them meet the requirements
                else:
                    # android or iOS
                    ext = path.splitext(app_file)
                    if ext[1] == ".apk" or ext[1] == ".aab":
                        # android
                        app_path = os.path.join(settings.get_apps_dir(), app_file)
                        apk = APK(app_path)
                        app = {
                            "file_name": app_file,
                            "package": apk.package,
                            "version": apk.version_name,
                            "build": apk.version_code,
                            "platform": "android"
                        }
                        custom_id = f"android-{apk.package}-{apk.version_name}"
                        print(f"Uploading {app_path}")
                        uploaded_app = AppsApi.upload_app(app_path, custom_id=custom_id)
                        app["app_url"] = uploaded_app.app_url
                        app["custom_id"] = uploaded_app.custom_id
                        settings.get_config().apps.append(app)
                        settings.save_config()
                        return app
                    elif ext[1] == ".ipa":
                        # iOS
                        # todo Implement iOS apps
                        app = {}
                    else:
                        continue

    @classmethod
    def bootstrap(cls, settings):
        conf = bsapi.configuration.BSAPIConf()
        conf.desired_caps = [
            {
                "dc_name": "Example",
                "name": "BSAPI Session",
                "build": "Python Android",
                "device": "Samsung Galaxy S8 Plus",
                "project": "BrowserStack Rest API",
                "browserstack.networkLogs": "true",
                "browserstack.deviceLogs": "true",
                "browserstack.appiumLogs": "true",
                "browserstack.video": "true"
            }
        ]

        if os.path.isfile(os.path.join(settings.base_dir, cls.conf_file_name)) is False:
            cls.save_config(settings, conf)


def connect(platform=None, package=None, version=None, caps=None, app_url=None) -> webdriver:
    """

    :param platform:
    :param package:
    :param version:
    :param caps:
    :param app_url:
    :return:
    """
    from bsapi import Settings
    if caps is None:
        raise ValueError("Caps is required")
    if platform is not None and package is None and version is None:
        raise ValueError("If platform is set, package and version is required")
    if platform is not None and package is not None and version is None:
        raise ValueError("If platform and package is set, version is required")
    if platform is None and package is not None and version is None:
        raise ValueError("If package is set, platform and version is required")
    if platform is None and package is not None and version is not None:
        raise ValueError("If package and version is set, platform is required")
    if platform is None and package is None and version is not None:
        raise ValueError("If version is set, platform and package is required")
    if platform is not None and package is None and version is not None:
        raise ValueError("If platform and version is set, package is required")

    dc_entries = Settings.get_config().desired_caps
    dc_entries = [dc for dc in dc_entries if dc["dc_name"] == caps]
    if len(dc_entries) > 0:
        desired_caps = dc_entries[0]
    else:
        raise ValueError(f"Desired Caps for {caps} not found in config")

    if app_url is not None:
        desired_caps["app"] = app_url
    elif platform is not None and package is not None and version is not None and app_url is None:
        desired_caps["app"] = Settings.get_app(platform, package, version)["app_url"]
    else:
        raise ValueError("If app_url is None platform, package, and version must be provided")

    url = f"https://{Settings.username}:{Settings.password}@hub-cloud.browserstack.com/wd/hub"
    driver = webdriver.Remote(url, desired_caps)
    return driver


def appium_test_suite(f, platform=None, package=None, version=None, caps=None, app_url=None):
    @functools.wraps
    def wrapper(*args, **kwargs):
        driver = connect(platform, package, version, caps, app_url)
        kwargs["driver"] = driver
        f(*args, **kwargs)
        driver.quit()

    return wrapper
