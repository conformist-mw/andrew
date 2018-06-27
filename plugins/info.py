from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.commands.add_command('info', 'Показывает сервисную информацию о пользователе', self.handler)

    def get_description(self):
        return 'Показывает серисную информацию о пользователе'

    def is_visible(self):
        return True

    async def handler(self, message):
        string = 'Информация о пользователе {}:\n'.format(message.raw['from']['username'])
        string += 'Протокол: *{}*\n'.format(message.connection.protocol)
        string += 'ID пользователя: *{}*\n'.format(message.raw['from']['id'])
        await message.send_back(string)
