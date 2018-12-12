import abc


class AbstractConnector:
    __metaclass__ = abc.ABCMeta

    def __init__(self, andrew=None):
        self.andrew = andrew
        self.public = True

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def connect(self, config):
        pass
