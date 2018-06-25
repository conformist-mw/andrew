class Plugins:

    def __init__(self, andrew):
        self.andrew = andrew
        self.plugins = {}

    def add_plugin(self, name):
        if name in self.plugins:
            raise Exception('Plugin {} already registered'.format(name))
        mod = __import__(name)
        plugin = mod.Plugin(self.andrew)
        plugin.register()
        self.plugins[name] = plugin
