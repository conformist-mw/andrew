class AbstractMessage:
    def __init__(self):
        self.connection = None
        self.sender = None
        self.text = None
        self.raw = None

    async def send_back(self, text):
        pass

    def get_id(self):
        return None

    def from_groupchat(self):
        return False

    def is_reply(self):
        return False

    def get_groupchat_id(self):
        return None

    def get_reply_message(self):
        return None
