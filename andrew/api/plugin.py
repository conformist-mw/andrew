import abc
import inspect
import os


class AbstractPlugin:
    __metaclass__ = abc.ABCMeta

    def __init__(self, andrew=None):
        self.andrew = andrew

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
        if self.andrew is None:
            raise EnvironmentError('Plugin don\'t initialized!')

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.database[os.path.basename(module.__file__).replace('.py', '')]

    def set_settings(self, default):
        if self.andrew is None:
            raise EnvironmentError('Plugin don\'t initialized!')

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.settings.register(os.path.basename(module.__file__).replace('.py', ''), default)

    def get_settings(self, chat):
        if self.andrew is None:
            raise EnvironmentError('Plugin don\'t initialized!')

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return self.andrew.settings.get(os.path.basename(module.__file__).replace('.py', ''), chat)
