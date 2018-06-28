import asyncio

from andrew.api.plugin import AbstractPlugin
from tinydb import Query
from tinydb.operations import increment


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew
        self.db = self.get_db()

    def register(self):
        self.andrew.commands.add_command('karma', 'Показывает текущую карму пользователя', self.command_handler)
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Управляет кармой пользователя'

    def is_visible(self):
        return True

    async def command_handler(self, message):
        karma = await self.get_karma(message, message.sender)
        string = 'Твоя карма: {}'.format(karma)
        await message.send_back(string)

    async def filter_handler(self, message):
        if message.from_groupchat() and message.is_reply():
            if message.text.startswith('++'):
                if message.get_reply_message().from_bot():
                    await message.send_back('Нельзя изменять карму боту!')
                    return True

                if message.get_reply_message().sender == message.sender:
                    await message.send_back('Нельзя изменять карму самому себе!')
                    return True

                await self.change_karma(message, 1)
                await message.send_back('Поднял карму пользователю до {}!'.format(
                                        await self.get_karma(message, message.get_reply_message().sender)))
            elif message.text.startswith('--') or message.text.startswith('—'):
                if message.get_reply_message().from_bot():
                    await message.send_back('Нельзя изменять карму боту!')
                    return True

                if message.get_reply_message().sender == message.sender:
                    await message.send_back('Нельзя изменять карму самому себе!')
                    return True

                await self.change_karma(message, -1)
                await message.send_back('Опустил карму пользователю до {}!'.format(
                                        await self.get_karma(message, message.get_reply_message().sender)))

    async def get_karma(self, message, sender_id):
        table = self.db.table(str(message.get_groupchat_id()))
        karma = table.search(Query().sender_id == sender_id)
        if not karma:
            table.insert({'sender_id': sender_id, 'karma': 0})
            karma = 0
        else:
            karma = karma[0]['karma']
        return karma

    async def change_karma(self, message, diff):
        karma = await self.get_karma(message, message.get_reply_message().sender)

        table = self.db.table(str(message.get_groupchat_id()))
        table.update({'karma': karma + diff}, Query().sender_id == message.get_reply_message().sender)
