from abc import ABC, abstractmethod


class BSAPIConf:
    def __init__(self):
        self.apps = []
        self.desired_caps = []
        self.media = []


class ConfigLoader(ABC):

    @classmethod
    @abstractmethod
    def get_config(cls, settings, config) -> BSAPIConf:
        pass

    @classmethod
    @abstractmethod
    def save_config(cls, settings, config):
        pass

    @classmethod
    @abstractmethod
    def get_app(cls, settings, plateform, package, build):
        pass

    @classmethod
    @abstractmethod
    def bootstrap(cls, settings):
        pass
