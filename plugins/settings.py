from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def pre_connect(self):
        self.andrew.commands.add_command('settings', 'Изменяет настройки плагинов бота', self.settings_handler,
                                         is_admin=True)

    def get_description(self):
        return 'Изменение настроек плагинов бота'

    def is_visible(self):
        return True

    async def settings_handler(self, message):
        args = message.text.split(' ')[1:]
        if len(args) < 1:
            await message.send_back('Не передано имя плагина')
            return

        plugin_name = args[0]
        if not self.andrew.plugins.is_exists(plugin_name):
            await message.send_back('Плагин {} не найден'.format(plugin_name))
            return

        if len(args) < 3:
            # Show all settings
            settings = self.andrew.settings.get(plugin_name, message.get_groupchat_id())
            settings_all = settings.get_all()
            string = 'Список настроек плагина:\n'
            for setting in settings_all:
                string += '{}: {}\n'.format(setting, settings_all[setting])
            self.andrew.logger.info(string)
            await message.send_back(string)
            return

        action = args[1]
        if action == 'set':
            if len(args) < 4:
                await message.send_back('Недостаточно аргументов')
                return
            try:
                settings = self.andrew.settings.get(plugin_name, message.get_groupchat_id())
                value = args[3:len(args)]
                value = ' '.join(value)
                settings.update(args[2], value)
                await message.send_back('{}: {}'.format(args[2], value))
            except KeyError:
                await message.send_back('Переданный ключ не существует')
        elif action == 'get':
            try:
                settings = self.andrew.settings.get(plugin_name, message.get_groupchat_id())
                setting = settings.get(args[2])
                await message.send_back(setting)
            except KeyError:
                await message.send_back('Переданный ключ не существует')
        else:
            await message.send_back('Не удалось распознать действие')
