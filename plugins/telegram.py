from aiotg import Bot
from andrew.api.connector import AbstractConnector
from andrew.api.message import AbstractMessage


class Plugin(AbstractConnector):

    def __init__(self, andrew):
        self.andrew = andrew
        self._bot = None
        self.protocol = 'telegram'

    def register(self):
        self.andrew.connections.add_connector(self)

    def get_description(self):
        return "Плагин для поддержки Telegram-чатов"

    def is_visible(self):
        return True

    def connect(self, config):
        self._bot = Bot(api_token=config['token'])
        self._bot.default_in_groups = True
        self._bot.default(self.handler)
        return self._bot.loop

    async def handler(self, chat, message):
        msg = Message()

        msg.connection = self
        msg.sender = message['from']['id']
        msg.text = message['text']
        msg.raw = message

        await self.andrew.handle_message(msg)

    async def send_message(self, destination, text, reply_to=None):
        self._bot.send_message(destination, text, reply_to_message_id=reply_to, parse_mode='Markdown')


class Message(AbstractMessage):
    async def send_back(self, text):
        if self.is_groupchat():
            await self.connection.send_message(self.raw['chat']['id'], text, self.raw['message_id'])
        else:
            await self.connection.send_message(self.sender, text)

    def is_groupchat(self):
        return self.raw['chat']['id'] < 0

    def is_reply(self):
        return 'reply_to_message' in self.raw
