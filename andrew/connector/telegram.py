from aiotg import Bot
from andrew.connector.message import Message


class TelegramConnector:

    def __init__(self, name, andrew):
        self.name = name
        self.andrew = andrew
        self.bot = None
        self.callbacks = {}

    def pre_connect(self):
        self.andrew.connections.add_connector(self)

    def connect(self, config):
        proxy = None
        if 'proxy' in config:
            self.andrew.logger.info('{}: connecting through proxy'.format(config['token']))
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
        return await self.bot.send_message(destination, text, reply_to_message_id=reply_to, parse_mode='Markdown')
