import asyncio
import time

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew
        self.db = self.get_db()

    def register(self):
        self.andrew.commands.add_command('ignore', 'Добавить или удалить пользователя из игнора', self.command_handler, is_moder=True)
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Позволяет боту игнорировать пользователей'

    def is_visible(self):
        return True

    async def command_handler(self, message):
        await message.send_back(message.connection.bot.api_call("getChatAdministrators", chat_id=int(message.raw['chat']['id'])))

    async def filter_handler(self, message):
        self.andrew.logger.info(message.raw)
