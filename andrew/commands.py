class Commands:

    def __init__(self):
        self._commands = {}

    def add_command(self, name, handler):
        if name in self._commands:
            raise Exception('Command {} already registered'.format(name))
        self._commands[name] = handler

    def is_exists(self, name):
        return name in self._commands

    async def execute(self, name, msg):
        if name not in self._commands:
            raise Exception('Command {} not found'.format(name))

        await self._commands[name](msg)
