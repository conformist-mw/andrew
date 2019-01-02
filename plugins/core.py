import asyncio
import time

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        super().__init__(andrew)

    def pre_connect(self):
        self.andrew.commands.add_command('ping', 'Отправляет "Pong!" в ответ', self.ping_handler)
        self.andrew.commands.add_command('plugins', 'Показывает список загруженных плагинов', self.plugins_handler)
        self.andrew.commands.add_command('commands', 'Показывает список доступных команд', self.commands_handler)
        self.andrew.commands.add_command('info', 'Показывает сервисную информацию о пользователе', self.info_handler)

    def get_description(self):
        return 'Базовая сервисная функциональность'

    async def ping_handler(self, message):
        await message.send_back('Pong!')

    async def plugins_handler(self, message):
        # TODO(spark): show only visible and enabled in chat plugins
        plugins = self.andrew.plugins.plugins

        string = 'Список доступных плагинов:\n'
        for plugin in plugins:
            if plugins[plugin].public:
                string += '*{}* - {}\n'.format(plugin, plugins[plugin].get_description())
        await message.send_back(string)

    async def commands_handler(self, message):
        commands = self.andrew.commands

        string = 'Список доступных команд:\n'
        for command in commands.commands:
            string += '*{}{}* - {}\n'.format(self.andrew.config['COMMAND_SYMBOL'], command, commands.commands_help[command])
        await message.send_back(string)

    async def info_handler(self, message):
        user = message.sender
        string = 'Информация о пользователе {}:\n'.format(user.raw['username'])
        string += 'ID пользователя: *{}*\n'.format(user.get_id())
        await message.send_back(string)
