from tinydb import Query


class Settings:
    def __init__(self, andrew):
        self.andrew = andrew
        self.plugins = {}

    def register(self, plugin, default):
        if plugin in self.plugins:
            raise Exception('Plugin {} already exposed their settings!'.format(plugin))

        self.plugins[plugin] = SettingsProvider(self.andrew.database['settings_{}'.format(plugin)], default)
        return self.plugins[plugin]

    def get(self, plugin):
        if plugin not in self.plugins:
            raise Exception('Plugin {} not exposed their settings!'.format(plugin))

        return self.plugins[plugin]


class SettingsProvider:
    def __init__(self, database, default):
        self.keys = default
        self.db = database

    def get(self, key):
        if key not in self.keys:
            raise Exception('Key {} is not found in settings provider!'.format(key))

        return self.keys[key]

    def get_all(self):
        return self.keys

    def set(self, key, value):
        if key not in self.keys:
            raise Exception('Key {} is not found in settings provider!'.format(key))

        self.keys[key] = value

    def update(self, key, value):
        if key not in self.keys:
            raise Exception('Key {} is not found in settings provider!'.format(key))
