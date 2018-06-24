import abc


class AbstractPlugin:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def is_visible(self):
        pass
