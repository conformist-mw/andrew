import asyncio
import time

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew
        self.db = self.get_db()

    def pre_connect(self):
        self.andrew.commands.add_command('ignore', 'Добавить или удалить пользователя из игнор-списка бота', self.ignore_handler, is_moder=True)
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Плагин модерации Telegram-чатов'

    def is_visible(self):
        return True

    async def ignore_handler(self, message):
        admins = await message.connection.bot.api_call("getChatAdministrators", chat_id=message.raw['chat']['id'])
        self.andrew.logger.info(admins)
        #await message.send_back(admins)
        pass

    async def filter_handler(self, message):
        pass
        #self.andrew.logger.info(message.raw)
