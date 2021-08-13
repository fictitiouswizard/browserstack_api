import os

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()


class Settings:
    username = os.getenv("browserstack_username")
    password = os.getenv("browserstack_key")
    proxies = {}
    verify_ssl = True

    @classmethod
    def auth(cls):
        return HTTPBasicAuth(cls.username, cls.password)

    @classmethod
    def request(cls):
        params = {"auth": Settings.auth()}
        if len(Settings.proxies) > 0:
            params["proxies"] = Settings.proxies
        if Settings.verify_ssl is False or isinstance(Settings.verify_ssl, str) is True:
            params["verify"] = Settings.verify_ssl

        return params

