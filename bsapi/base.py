import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def configure_sessions(retries, backoff):
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[404]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


class Api:
    """
    Base class to inherit requests configuration from
    """
    http = configure_sessions(8, 1)

    @classmethod
    def set_timeout(cls, retries, backoff_factor):
        """
        Set the number of times to try http requests

        :param retries:
        :type retries: int
        :param backoff_factor:
        :type retries: int
        """
        cls.session = configure_sessions(retries, backoff_factor)
