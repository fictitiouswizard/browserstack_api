import unittest
from requests.exceptions import HTTPError

from bsapi.app_automate.appium.devices import *


class TestDevicesApi(unittest.TestCase):

    def test_get_device_list(self):
        try:
            devices = DevicesApi.get_device_list()
            self.assertGreaterEqual(len(devices), 0, "Devices should be returned")
        except HTTPError as e:
            self.fail(f"Invalid Status Code returned: {e.response}")


if __name__ == "__main__":
    unittest.main()
