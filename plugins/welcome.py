from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        super().__init__(andrew)

        self.set_settings({
            'message': 'Привет, {}!'
        })

    def post_connect(self):
        connections = self.andrew.connections.connections
        for c in connections:
            connection = self.andrew.connections.connections[c]
            connection.add_handler('new_chat_member', self.new_member_handler)

    def get_description(self):
        return 'Приветствует вошедших пользователей'

    async def new_member_handler(self, connector, chat, message):
        nickname = message['first_name'] if 'first_name' in message else ''
        nickname += ' {}'.format(message['last_name']) if 'last_name' in message else ''
        msg = self.get_settings(chat.id).get('message')
        await chat.send_text(msg.format(nickname))
