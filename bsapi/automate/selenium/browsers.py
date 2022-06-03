from bsapi import Settings, Api
from bsapi.models import Browser


class BrowsersApi(Api):
    """Class for interacting with the Browsers REST endpoint on BrowserStack"""

    @classmethod
    def get_browser_list(cls):
        """
        Get a list of supported browsers

        Example::

            browsers = BrowsersApi.get_browser_list()
            for browser in browsers:
                print(browser.browser_os, browser.os_version, browser.browser)

        :return: a list of browsers supported by BrowserStack
        :rtype: [:class:`bsapi.models.Browser`
        """
        url = f"{Settings.base_url}/automate/browsers.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                Browser(
                    browser_os=j["os"],
                    os_version=j["os_version"],
                    browser=j["browser"],
                    device=j["device"],
                    browser_version=j["browser_version"],
                    real_mobile=j["real_mobile"]
                ) for j
                in rj
            ]
        else:
            response.raise_for_status()