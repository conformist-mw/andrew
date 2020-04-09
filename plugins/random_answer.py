from andrew.api.plugin import AbstractPlugin
from datetime import datetime


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        super().__init__(andrew)
        self.db = andrew.db

    def pre_connect(self):
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Отвечаю случайной фразой'

    async def filter_handler(self, message):
        if not message.is_reply() or not message.from_groupchat() or not message.get_reply_message().sender.is_bot():
            return
        with self.db as db:
            db.insert_message(context={
                'user_id': message.get_user_id(),
                'username': message.get_username(),
                'created': datetime.utcnow(),
                'message': message.text,
            })
            text = db.get_random_message()
        await message.send_back(text)
