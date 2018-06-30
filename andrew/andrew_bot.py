import logging
import os
import sys
import signal

from andrew.filters import Filters
from andrew.plugins import Plugins
from .connections import Connectons
from .commands import Commands
from .config import Config
from .database import Database


class AndrewBot(object):
    def __init__(self):
        self.config = Config()
        self.database = Database(self)
        self.logger = logging.getLogger()

        self.plugins = Plugins(self)
        self.connections = Connectons(self)
        self.commands = Commands()
        self.filters = Filters()

    def run(self):
        self.init_logging()
        self.logger.info('Starting AndrewBot')
        signal.signal(signal.SIGTERM, self.stop)
        self.load()

    def stop(self):
        self.logger.info('Stopping bot')
        self.unload()

        sys.exit(0)

    def load(self):
        self.logger.info('Init plugins')
        self.plugins.scan_plugins(self.config['PLUGINS_PATH'])

        self.logger.info('Start connections')
        self.connections.connect(self.config['CONNECTIONS'])

    def unload(self):
        for t in self.connections.tasks:
            t.cancel()
        for d in self.database.cache:
            self.database.cache[d].close()

    async def handle_message(self, msg):
        if await self.filters.execute(msg) is False:
            return

        if msg.text.startswith(self.config['COMMAND_SYMBOL']) and len(msg.text) > 1 and msg.text[1] is not ' ':
            await self.handle_command(msg)

    async def handle_command(self, msg):
        command = msg.text[1:]

        # TODO(spark): implement admin commands and security checks
        if self.commands.is_exists(command):
            await self.commands.execute(command, msg)
        else:
            await msg.send_back('Команда не найдена!')

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
