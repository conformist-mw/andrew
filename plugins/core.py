import asyncio
import time

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew
        self.db = self.get_db()

    def register(self):
        self.andrew.commands.add_command('ping', 'Отправляет "Pong!" в ответ', self.ping_handler)
        self.andrew.commands.add_command('plugins', 'Показывает список загруженных плагинов', self.plugins_handler)
        self.andrew.commands.add_command('commands', 'Показывает список доступных команд', self.commands_handler)
        self.andrew.commands.add_command('info', 'Показывает сервисную информацию о пользователе', self.info_handler)

    def get_description(self):
        return 'Базовая сервисная функциональность'

    def is_visible(self):
        return True

    async def ping_handler(self, message):
        await message.send_back('Pong!')

    async def plugins_handler(self, message):
        # TODO(spark): show only visible and enabled in chat plugins
        plugins = self.andrew.plugins.plugins

        string = 'Список доступных плагинов:\n'
        for plugin in plugins:
            string += '*{}* - {}\n'.format(plugin, plugins[plugin].get_description())
        await message.send_back(string)

    async def commands_handler(self, message):
        commands = self.andrew.commands

        string = 'Список доступных команд:\n'
        for command in commands.commands:
            string += '*{}{}* - {}\n'.format(self.andrew.config['COMMAND_SYMBOL'], command, commands.commands_help[command])
        await message.send_back(string)

    async def info_handler(self, message):
        string = 'Информация о пользователе {}:\n'.format(message.raw['from']['username'])
        string += 'Протокол: *{}*\n'.format(message.connection.protocol)
        string += 'ID пользователя: *{}*\n'.format(message.raw['from']['id'])
        await message.send_back(string)