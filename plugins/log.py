import asyncio
import time

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        super().__init__(andrew)

        self.set_settings({
            'enabled': True,
        })

    def pre_connect(self):
        self.andrew.filters.add_filter(self.log_filter)

    def get_description(self):
        return 'Пишет сообщения чата в лог'

    async def log_filter(self, message):
        enabled = bool(self.get_settings(message.get_groupchat_id()).get('enabled'))
        if enabled:
            if message.from_groupchat():
                self.andrew.logger.info(f'LOG [{message.get_groupchat_id()}] [{message.sender.get_nickname()}: '
                                        f'{message.text}')
            else:
                self.andrew.logger.info(f'LOG [{message.get_groupchat_id()}] [{message.sender.get_nickname()}: '
                                        f'{message.text}')
