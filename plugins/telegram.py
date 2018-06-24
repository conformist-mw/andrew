from aiotg import Bot
from andrew.api.connector import AbstractConnector
from andrew.api.message import Message


class Plugin(AbstractConnector):

    def __init__(self, andrew):
        self.andrew = andrew
        self._bot = None

    def register(self):
        self.andrew.connections.add_connector('telegram', self)

    def get_description(self):
        return "A plugin to support Telegram chats"

    def is_visible(self):
        return True

    def connect(self, config):
        self._bot = Bot(api_token=config['token'])
        self._bot.default(self.handler)
        return self._bot.loop

    async def handler(self, chat, message):
        msg = Message()

        msg.connection = self
        msg.sender = message['from']['id']
        msg.text = message['text']
        msg.raw = message

        await self.andrew.handle_message(msg)

    async def send_message(self, destination, text):
        self._bot.send_message(destination, text)
