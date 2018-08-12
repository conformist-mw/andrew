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

    def pre_connect(self):
        pass

    def post_connect(self):
        pass

    def get_db(self):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.database[os.path.basename(module.__file__).replace('.py', '')]

    def get_settings(self, default):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.settings.register(os.path.basename(module.__file__).replace('.py', ''), default)
