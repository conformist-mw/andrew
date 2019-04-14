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
        app.add_routes([
            web.post('/notify', self.notify_handler),
            web.get('/app', self.get_apps_handler),
            web.get('/app/{uuid}', self.get_app_handler),
            web.post('/app', self.post_app_handler),
            web.delete('/app/{uuid}', self.delete_app_handler)
        ])

        runner = web.AppRunner(app)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, self.host, self.port)
        loop.run_until_complete(site.start())

    def get_description(self):
        return 'UW Notifier'

    def pre_connect(self):
        self.andrew.commands.add_command('notifier', 'Отправляет Notifier UUID чата в ответ', self.register_handler)

    async def register_handler(self, message):
        chat_id = message.get_groupchat_id()
        chats_table = self.db.table('chats')
        row = chats_table.search(Query().chat_id == chat_id)
        if not row:
            u = uuid.uuid4()
            chats_table.insert({'chat_id': chat_id, 'uuid': str(u), 'connector': message.connection.name})
        else:
            u = row[0]['uuid']
        await message.send_back(f'UUID этого чата: *{str(u)}*')

    async def notify_handler(self, request):
        data = await request.post()

        if 'uuid' in data and 'app' in data and 'text' in data:
            apps_table = self.db.table('apps')
            app_row = apps_table.search(Query().uuid == data['app'])
            if not app_row:
                return web.json_response({'error': True, 'message': 'Given chat UUID not found'},
                                         status=404)
            app_row = app_row[0]

            chats_table = self.db.table('chats')
            chat_row = chats_table.search(Query().uuid == data['uuid'])
            if not chat_row:
                return web.json_response({'error': True, 'message': 'Given chat UUID not found'},
                                         status=404)
            chat_row = chat_row[0]

            await self.andrew.connections.connections[chat_row['connector']]\
                .send_message(chat_row['chat_id'], f'*Уведомление от {app_row["name"]}*\n{data["text"]}')

            return web.json_response({
                'uuid': data['uuid'],
                'app': data['app'],
                'app_name': app_row['name'],
                'text': data['text']
            })

        else:
            return web.json_response({
                'error': True,
                'message': 'Both chat and app UUID\'s and text parameters are required'
            }, status=400)

    async def get_apps_handler(self, request):
        chats_table = self.db.table('chats')
        rows = chats_table.all()
        print(rows)
        return web.json_response(rows)

    async def get_app_handler(self, request):
        pass

    async def post_app_handler(self, request):
        data = await request.post()

        if 'name' in data:
            apps_table = self.db.table('apps')
            obj = {'name': data['name'], 'uuid': str(uuid.uuid4())}
            apps_table.insert(obj)

            return web.json_response(obj)
        else:
            return web.json_response({'error': True, 'message': 'name parameter is required'}, status=400)

    async def delete_app_handler(self, request):
        pass
