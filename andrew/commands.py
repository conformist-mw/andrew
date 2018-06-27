class Commands:

    def __init__(self):
        self.commands = {}
        self.commands_help = {}

    def add_command(self, name, help, handler):
        if name in self.commands:
            raise Exception('Command {} already registered'.format(name))
        self.commands[name] = handler
        self.commands_help[name] = help

    def is_exists(self, name):
        return name in self.commands

    async def execute(self, name, msg):
        if name not in self.commands:
            raise Exception('Command {} not found'.format(name))

        await self.commands[name](msg)
