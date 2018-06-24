class Message:
    def __init__(self):
        self.connection = None
        self.sender = None
        self.text = None
        self.raw = None

    async def send_back(self, text):
        await self.connection.send_message(self.sender, text)
