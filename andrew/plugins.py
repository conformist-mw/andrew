import os
import sys

from andrew.api.plugin import AbstractPlugin


class Plugins:

    def __init__(self, andrew):
        self.andrew = andrew
        self.plugins = {}

    def add_plugin(self, name):
        if name in self.plugins:
            raise Exception('Plugin {} already registered'.format(name))
        mod = __import__(name)
        plugin = mod.Plugin(self.andrew)
        plugin.pre_connect()
        self.plugins[name] = plugin

    def scan_plugins(self, plugins_path):
        path = plugins_path
        sys.path.insert(0, path)
        for f in os.listdir(path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                self.add_plugin(fname)
        sys.path.pop(0)

    def post_connect(self):
        for p in self.plugins:
            if isinstance(self.plugins[p], AbstractPlugin):
                self.plugins[p].post_connect()
