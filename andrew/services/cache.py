import time


class Cache:
    def __init__(self, andrew):
        self.andrew = andrew
        self.storage = {}
        self.storage_timeouts = {}

    def save(self, key, value, duration=60):
