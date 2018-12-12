from tinydb import Query


class Settings:
    def __init__(self, andrew):
        self.andrew = andrew
        self.plugins = {}
        self.plugins_defaults = {}

    def register(self, plugin, default):
        if plugin in self.plugins:
            raise KeyError('Plugin {} already exposed their settings!'.format(plugin))

        self.plugins_defaults[plugin] = default

    def get(self, plugin, chat):
        if plugin not in self.plugins_defaults:
            raise KeyError('Plugin {} not exposed their settings!'.format(plugin))

        if chat not in self.plugins:
            self.plugins[plugin] = SettingsProvider(self.andrew.database[
                                                        'settings_{}'.format(str(chat))].table(str(plugin)),
                                                    self.plugins_defaults[plugin])
        return self.plugins[plugin]


class SettingsProvider:
    def __init__(self, table, default):
        self.keys = dict(default)
        self.db = table
        for rec in table.all():
            self.keys[rec['key']] = rec['value']

    def get(self, key):
        if key not in self.keys:
            raise KeyError('Key {} is not found in settings provider!'.format(key))

        return self.keys[key]

    def get_all(self):
        return self.keys

    def set(self, key, value):
        if key not in self.keys:
            raise KeyError('Key {} is not found in settings provider!'.format(key))

        self.keys[key] = value

    def update(self, key, value):
        if key not in self.keys:
            raise KeyError('Key {} is not found in settings provider!'.format(key))

        self.db.upsert({'key': key, 'value': value}, Query().key == key)
        self.set(key, value)
