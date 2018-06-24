from import_string.base import import_string


class Config(dict):
    def apply(self, cfg):
        obj = import_string(cfg)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class BaseConfig(object):
    DEBUG = False

    LOG_TO_FILE = True
    LOG_FILENAME = 'bot.log'

    PLUGINS_PATH = 'plugins'

    COMMAND_SYMBOL = '!'

    ADMINS = []

    CONNECTIONS = {}
