from bsapi import Settings, Api


class Device:
    def __init__(self, os=None, os_version=None, device=None, real_mobile=None):
        self.os = os
        self.os_version = os_version
        self.device = device
        self.real_mobile = real_mobile


class DevicesApi(Api):

    @classmethod
    def get_device_list(cls):
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