from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.commands.add_command('commands', 'Показывает список доступных команд', self.handler)

    def get_description(self):
        return 'Показывает список доступных команд'

    def is_visible(self):
        return True

    async def handler(self, message):
        # TODO(spark): show only visible and enabled in chat plugins
        commands = self.andrew.commands

        string = 'Список доступных команд:\n'
        for command in commands.commands:
            string += '*{}{}* - {}\n'.format(self.andrew.config['COMMAND_SYMBOL'], command, commands.commands_help[command])
        await message.send_back(string)
