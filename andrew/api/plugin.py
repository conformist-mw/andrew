import abc
import inspect
import os


class AbstractPlugin:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def is_visible(self):
        pass

    def get_db(self):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.database[os.path.basename(module.__file__)]
