class AbstractMessage:
    def __init__(self):
        self.connection = None
        self.sender = None
        self.text = None
        self.raw = None

    async def send_back(self, text):
        pass

    def from_groupchat(self):
        return False

    def from_bot(self):
        return False

    def is_reply(self):
        return False

    def get_groupchat_id(self):
        return 0

    def get_reply_message(self):
        return None

    def get_nickname(self):
        return None
