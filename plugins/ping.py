from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.commands.add_command('ping', self.handler)

    def get_description(self):
        return 'Отправляет "Pong!" в ответ'

    def is_visible(self):
        return True

    async def handler(self, message):
        await message.send_back('Pong!')
