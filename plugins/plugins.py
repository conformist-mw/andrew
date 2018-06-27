from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.commands.add_command('plugins', 'Показывает список загруженных плагинов', self.handler)

    def get_description(self):
        return 'Показывает список загруженных плагинов'

    def is_visible(self):
        return True

    async def handler(self, message):
        # TODO(spark): show only visible and enabled in chat plugins
        plugins = self.andrew.plugins.plugins

        string = 'Список доступных плагинов:\n'
        for plugin in plugins:
            string += '*{}* - {}\n'.format(plugin, plugins[plugin].get_description())
        await message.send_back(string)
