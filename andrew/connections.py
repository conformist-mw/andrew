import asyncio


class Connectons:
    def __init__(self, andrew):
        self.andrew = andrew

        self._connectors = {}
        self._connections = {}
        self._tasks = []

    def add_connector(self, connector):
        if connector.protocol in self._connectors:
            raise Exception('Connector with protocol {} already exists'.format(connector.protocol))
        self._connectors[connector.protocol] = connector

    def connect(self, connections):
        # Start new asyncio loop
        loop = asyncio.get_event_loop()

        for c in connections:
            # Find connector
            connection = connections[c]
            if connection['protocol'] not in self._connectors:
                raise Exception('Connector {} not found'.format(connection['protocol']))

            # Create new connector instance
            connector = self._connectors[connection['protocol']].__class__(self.andrew)
            self._tasks.append(loop.create_task(connector.connect(connection)()))
            self._connections[c] = connection
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            for t in self._tasks:
                t.cancel()
            for d in self.andrew.database.cache:
                self.andrew.database.cache[d].close()
