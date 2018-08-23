import asyncio
import time

from aiotg import BotApiError

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew
        self.db = self.get_db()
        self.set_settings({
            'cooldown': 10,
            'incmessage': 'Поднял карму {} до {}!',
            'decmessage': 'Опустил карму {} до {}!',
        })

        self.cooldown_cache = {}

    def pre_connect(self):
        self.andrew.commands.add_command('karma', 'Показывает текущую карму пользователя', self.karma_handler)
        self.andrew.commands.add_command('karmatop', 'Показывает топ кармы в чате', self.karmatop_handler)
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Управляет кармой пользователя'

    def is_visible(self):
        return True

    async def karma_handler(self, message):
        if message.from_groupchat():
            karma = await self.get_karma(message, message.sender)
            string = 'Твоя карма: {}'.format(karma)
            await message.send_back(string)
        else:
            await message.send_back('Карма работает только в групповом чате!')

    async def karmatop_handler(self, message):
        if message.from_groupchat():
            # Very unoptimized, but works

            # TODO(spark): works only for telegram now
            table = self.db.table(str(message.get_groupchat_id()))
            members = sorted(table.all(), key=lambda i: i['karma'], reverse=True)[0:10]

            string = 'Топ беседы:\n'
            for member in members:
                try:
                    member_info = await message.connection.bot.api_call("getChatMember",
                                                                        chat_id=message.raw['chat']['id'],
                                                                        user_id=member['sender_id'])
                    member_name = member_info['result']['user']['first_name']
                    member_name += ' {}'.format(member_info['result']['user']['last_name']) \
                        if 'last_name' in member_info['result']['user'] else ''
                    string += '{} - {}\n'.format(member_name, member['karma'])
                except BotApiError:
                    string += '<недоступно> - {}\n'.format(member['karma'])
            await message.send_back(string)
        else:
            await message.send_back('Карма работает только в групповом чате!')

    async def filter_handler(self, message):
        if message.from_groupchat() and message.is_reply():
            if message.text.startswith('++'):
                checks = await self.checks(message)
                if not checks:
                    return True

                await self.change_karma(message, 1)
                await message.send_back(self.get_settings(message.get_groupchat_id()).get('incmessage').format(
                    message.get_reply_message().sender.get_nickname(),
                    await self.get_karma(message, message.get_reply_message().sender)))
            elif message.text.startswith('--') or message.text.startswith('—'):
                if not await self.checks(message):
                    return True

                await self.change_karma(message, -1)
                await message.send_back(self.get_settings(message.get_groupchat_id()).get('decmessage').format(
                    message.get_reply_message().sender.get_nickname(),
                    await self.get_karma(message, message.get_reply_message().sender)))

    async def get_karma(self, message, sender):
        sender_id = sender.get_id()
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
        table.update({'karma': karma + diff}, Query().sender_id == message.get_reply_message().sender.get_id())

    async def checks(self, message):
        sender_id = message.sender.get_id()
        if message.get_reply_message().sender.is_bot():
            await message.send_back('Нельзя изменять карму боту!')
            return False

        if message.get_reply_message().sender.get_id() == sender_id:
            await message.send_back('Нельзя изменять карму самому себе!')
            return False

        if sender_id in self.cooldown_cache:
            cooldown = self.get_settings(message.get_groupchat_id()).get('cooldown')
            if time.time() - self.cooldown_cache[sender_id] < int(cooldown):
                await message.send_back('Нельзя изменять карму так часто!')
                return False

        self.cooldown_cache[sender_id] = time.time()
        return True
