class Commands:

    def __init__(self):
        self.commands = {}
        self.commands_help = {}
        self.moder_commands = []
        self.admin_commands = []

    def add_command(self, name, description, handler, is_moder=False, is_admin=False):
        if name in self.commands:
            raise Exception('Command {} already registered'.format(name))
        self.commands[name] = handler
        self.commands_help[name] = description

        if is_moder:
            self.moder_commands.append(name)

        if is_admin:
            self.admin_commands.append(name)

    def is_exists(self, name):
        return name in self.commands

    async def execute(self, name, msg):
        if name not in self.commands:
            raise Exception('Command {} not found'.format(name))

        await self.commands[name](msg)
