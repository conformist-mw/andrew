from aiohttp import web
import uuid

from andrew.api.plugin import AbstractPlugin
from tinydb import Query


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        super().__init__(andrew)

        self.db = self.get_db()

        self.host = '0.0.0.0'
        self.port = 8081

        loop = andrew.connections.loop
        app = web.Application()
        app.add_routes([web.post('/notify', self.handle)])

        runner = web.AppRunner(app)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.host, self.port)
        loop.run_until_complete(site.start())

    def get_description(self):
        return 'UW Notifier'

    def pre_connect(self):
        self.andrew.commands.add_command('notifier', 'Отправляет "Pong!" в ответ', self.register_handler)

    async def register_handler(self, message):
        chat_id = message.get_groupchat_id()
        row = self.db.search(Query().chat_id == chat_id)
        if not row:
            u = uuid.uuid4()
            self.db.insert({'chat_id': chat_id, 'uuid': str(u), 'connector': message.connection.name})
        else:
            u = row[0]['uuid']
        await message.send_back(f'UUID этого канала: {str(u)}')

    async def handle(self, request):
        data = await request.post()
        if 'uuid' in data and 'text' in data:
            row = self.db.search(Query().uuid == data['uuid'])
            if not row:
                return web.Response(text='404 UUID not found\n')

            row = row[0]
            await self.andrew.connections.connections[row['connector']]\
                .send_message(row['chat_id'], f'*Уведомление*\n{data["text"]}')
            return web.Response(text='200 OK\n')
        else:
            return web.Response(text='403 Access denied\n')
