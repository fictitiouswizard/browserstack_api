from bsapi import Settings, Api


class Device:
    """
    Represents a supported device on BrowserStack

    :param str os: The OS running on the device
    :param str os_version: The version number for the devices OS
    :param str device: The name of the device
    :param str real_mobile: Is the device a real phone
    """
    def __init__(self, os=None, os_version=None, device=None, real_mobile=None):
        self.os = os
        self.os_version = os_version
        self.device = device
        self.real_mobile = real_mobile


class DevicesApi(Api):
    """Class for interacting with the Devices REST endpoint on BrowserStack"""
    @classmethod
    def get_device_list(cls):
        """
        Gets a list of devices that support Appium on BrowserStack

        :return: List of supported devices
        :rtype: list[:class:`bsapi.app_automate.appium.devices.Device`]
        """
        url = f"{Settings.base_url}/app-automate/devices.json"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                Device(
                    os=d["os"],
                    os_version=d["os_version"],
                    device=d["device"],
                    real_mobile=d["realMobile"]
                )
                for d
                in rj
            ]
        else:
            response.raise_for_status()
