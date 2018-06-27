from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.commands.add_command('karma', 'Показывает текущую карму пользователя', self.command_handler)
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Управляет кармой пользователя'

    def is_visible(self):
        return True

    async def command_handler(self, message):
        string = 'Информация о пользователе {}:\n'.format(message.raw['from']['username'])
        string += 'Протокол: *{}*\n'.format(message.connection.protocol)
        string += 'ID пользователя: *{}*\n'.format(message.raw['from']['id'])
        await message.send_back(string)

    async def filter_handler(self, message):
        if message.is_groupchat():
            if message.connection.protocol == 'telegram':
                if 'reply_to_message' in message.raw:
                    if message.text == '++':
                        await message.send_back('blah')
                    elif message.text == '--':
                        print('karma minus')
            else:
                await message.send_back('Не реализованно для этого коннектора')
