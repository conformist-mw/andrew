import logging
import os
import sys
import time

from .connections import Connectons
from .commands import Commands
from .config import Config
from .database import Database


class AndrewBot(object):
    def __init__(self):
        self.config = Config()
        self.database = Database(self)
        self.logger = logging.getLogger()

        self.connections = Connectons(self)
        self.commands = Commands()
        self.filters = []
        self.admin_commands = []

        self.running = True

    def run(self):
        self.init_logging()
        self.logger.info('Starting AndrewBot')

        self.logger.info('Init plugins')
        self.init_plugins()

        self.logger.info('Start connections')
        self.connections.connect(self.config['CONNECTIONS'])

        self.logger.info('Stopping bot')

    def stop(self):
        self.running = False

    async def handle_message(self, msg):
        # TODO(spark): implement filters
        if msg.text.startswith(self.config['COMMAND_SYMBOL']) and len(msg.text) > 1 and msg.text[1] is not ' ':
            await self.handle_command(msg)

    async def handle_command(self, msg):
        command = msg.text[1:]

        # TODO(spark): implement admin commands and security checks
        if self.commands.is_exists(command):
            await self.commands.execute(command, msg)

    def init_logging(self):
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

        if self.config['DEBUG']:
            self.logger.setLevel(logging.DEBUG)

        if self.config['LOG_TO_FILE']:
            fh = logging.FileHandler(self.config['LOG_FILENAME'])
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def init_plugins(self):
        path = self.config['PLUGINS_PATH']
        sys.path.insert(0, path)
        for f in os.listdir(path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                self.logger.debug('Found plugin {}'.format(fname))
                mod = __import__(fname)
                mod.Plugin(self).register()
                self.logger.debug('Loaded plugin {}'.format(fname))
        sys.path.pop(0)