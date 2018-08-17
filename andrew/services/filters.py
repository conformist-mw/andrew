class Filters:

    def __init__(self):
        self.filters = []

    def add_filter(self, handler):
        self.filters.append(handler)

    async def execute(self, msg):
        for filt in self.filters:
            if await filt(msg) is False:
                return False
