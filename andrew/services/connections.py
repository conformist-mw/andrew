import asyncio

from andrew.connector.telegram import TelegramConnector


class Connectons:
    def __init__(self, andrew):
        self.andrew = andrew

        self.loop = asyncio.get_event_loop()
        self.connections = {}
        self.tasks = []

    def connect(self, connections):
        for c in connections:
            connection = connections[c]

            # Create new connector instance
            connector = TelegramConnector(self.andrew)
            self.tasks.append(self.loop.create_task(connector.connect(connection)()))
            self.connections[c] = connector

        self.andrew.plugins.post_connect()

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.andrew.stop()
