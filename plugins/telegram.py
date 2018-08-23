from aiotg import Bot
from andrew.api.connector import AbstractConnector
from andrew.api.message import AbstractMessage
from andrew.api.sender import AbstractSender


class Plugin(AbstractConnector):

    def __init__(self, andrew):
        self.andrew = andrew
        self.bot = None
        self.protocol = 'telegram'
        self.callbacks = {}

    def pre_connect(self):
        self.andrew.connections.add_connector(self)

    def get_description(self):
        return "Плагин для поддержки Telegram-чатов"

    def is_visible(self):
        return True

    def connect(self, config):
        proxy = None
        if 'proxy' in config:
            self.andrew.logger.info('{}: connecting using proxy'.format(config['token']))
            proxy = config['proxy']
        self.bot = Bot(api_token=config['token'], proxy=proxy)
        self.bot.default_in_groups = True
        self.bot.default(self.handler)
        return self.bot.loop

    def add_handler(self, msg_type, cb):
        async def _handler(chat, message):
            await cb(self, chat, message)

        self.bot.handle(msg_type)(_handler)

    async def handler(self, chat, message):
        msg = Message.build_from_raw(self, message)
        await self.andrew.handle_message(msg)

    async def send_message(self, destination, text, reply_to=None):
        self.bot.send_message(destination, text, reply_to_message_id=reply_to, parse_mode='Markdown')


class Message(AbstractMessage):
    async def send_back(self, text):
        if self.from_groupchat():
            await self.connection.send_message(self.raw['chat']['id'], text, self.raw['message_id'])
        else:
            await self.connection.send_message(self.sender, text)

    def from_groupchat(self):
        return self.raw['chat']['id'] < 0

    def is_reply(self):
        return 'reply_to_message' in self.raw

    def get_groupchat_id(self):
        return self.raw['chat']['id']

    def get_reply_message(self):
        return Message.build_from_raw(self.connection, self.raw['reply_to_message'])

    @staticmethod
    def build_from_raw(connection, raw):
        msg = Message()

        msg.connection = connection
        msg.sender = Sender.build_from_raw(raw['from']) if 'from' in raw else None
        msg.text = raw['text'] if 'text' in raw else ''
        msg.raw = raw
        return msg


class Sender(AbstractSender):
    def is_bot(self):
        return self.raw['is_bot']

    def get_id(self):
        return self.raw['id']

    def get_nickname(self):
        nickname = self.raw['first_name'] if 'first_name' in self.raw else ''
        nickname += ' {}'.format(self.raw['last_name']) if 'last_name' in self.raw else ''
        return nickname

    def is_moder(self):
        return False

    def is_admin(self):
        return False

    @staticmethod
    def build_from_raw(raw):
        sender = Sender()

        sender.raw = raw
        return sender
