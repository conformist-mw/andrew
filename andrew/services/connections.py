import asyncio

from andrew.connector import TelegramConnector


class Connectons:
    def __init__(self, andrew):
        self.andrew = andrew

        self.connections = {}
        self.tasks = []

    def connect(self, connections):
        # Start new asyncio loop
        loop = asyncio.get_event_loop()

        for c in connections:
            connection = connections[c]

            # Create new connector instance
            connector = TelegramConnector(self.andrew)
            self.tasks.append(loop.create_task(connector.connect(connection)()))
            self.connections[c] = connector

        self.andrew.plugins.post_connect()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.andrew.stop()
