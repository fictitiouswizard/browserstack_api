import os

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from from_root import from_root

from bsapi.config import BSAPIConf
import bsapi.app_automate.appium.utils

load_dotenv()


class Settings:
    """
    Configuration for the bsapi module
    """
    username = os.getenv("BROWSERSTACK_USERNAME")
    password = os.getenv("BROWSERSTACK_KEY")
    proxies = {}
    verify_ssl = True
    base_url = "https://api-cloud.browserstack.com"
    apps_dir = "apps"
    media_dir = "media"
    base_dir = from_root()
    conf_loader = bsapi.app_automate.appium.utils.AppiumJsonLoader
    __conf = None

    @classmethod
    def get_config(cls) -> BSAPIConf:
        if cls.__conf is None:
            cls.__conf = cls.conf_loader.get_config(cls, cls.__conf)
            return cls.__conf
        else:
            return cls.__conf

    @classmethod
    def save_config(cls):
        return cls.conf_loader.save_config(cls, cls.__conf)

    @classmethod
    def get_app(cls, platform, package, version):
        return cls.conf_loader.get_app(cls, platform, package, version)

    @classmethod
    def get_apps_dir(cls):
        return os.path.join(cls.base_dir, cls.apps_dir)

    @classmethod
    def get_media_dir(cls):
        return os.path.join(cls.base_dir, cls.apps_dir)

    @classmethod
    def auth(cls):
        """
        Returns an HTTPBasicAuth object using Settings.username and Settings.password

        :return: requests.auth.HTTPBasicAuth
        """
        return HTTPBasicAuth(cls.username, cls.password)

    @classmethod
    def request(cls):
        """
        Generate settings dict for requests calls

        :return: dict of settings
        :rtype: dict[string]
        """
        params = {"auth": Settings.auth()}
        if len(Settings.proxies) > 0:
            params["proxies"] = Settings.proxies
        if Settings.verify_ssl is False or isinstance(Settings.verify_ssl, str) is True:
            params["verify"] = Settings.verify_ssl

        return params

    @classmethod
    def bootstrap(cls):
        cls.conf_loader.bootstrap(cls)
        if os.path.isdir(os.path.join(cls.base_dir, cls.apps_dir)) is False:
            os.makedirs(os.path.join(cls.base_dir, cls.apps_dir))
        if os.path.isdir(os.path.join(cls.base_dir, cls.media_dir)) is False:
            os.makedirs(os.path.join(cls.base_dir, cls.apps_dir))


