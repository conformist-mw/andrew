from andrew.connector.sender import Sender


class Message:

    def __init__(self):
        self.connection = None
        self.sender = None
        self.text = None
        self.raw = None

    async def send_back(self, text):
        if self.from_groupchat():
            msg = await self.connection.send_message(self.raw['chat']['id'], text, self.raw['message_id'])
        else:
            msg = await self.connection.send_message(self.sender.get_id(), text, self.raw['message_id'])

        return Message.build_from_raw(self.connection, msg['result'])

    def get_id(self):
        return self.raw['message_id']

    def get_user_id(self):
        return self.raw['from']['id']

    def get_username(self):
        return self.raw['from']['username']

    def from_groupchat(self):
        return self.raw['chat']['id'] < 0

    def is_reply(self):
        return 'reply_to_message' in self.raw

    def get_groupchat_id(self):
        return self.raw['chat']['id']

    def get_reply_message(self):
        return Message.build_from_raw(self.connection, self.raw['reply_to_message'])

    def delete(self):
        return self.connection.bot.api_call(
            "deleteMessage", chat_id=self.get_groupchat_id(), message_id=self.get_id()
        )

    @staticmethod
    def build_from_raw(connection, raw):
        msg = Message()

        msg.connection = connection
        msg.sender = Sender.build_from_raw(raw['from']) if 'from' in raw else None
        msg.text = raw['text'] if 'text' in raw else ''
        msg.raw = raw
        return msg
