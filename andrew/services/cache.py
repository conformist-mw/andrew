import time


class Cache:
    def __init__(self, andrew):
        self.andrew = andrew
        self.storage = {}
        self.storage_timeouts = {}

    def save(self, key, value, duration=60):
        self.storage[key] = value
        self.storage_timeouts[key] = time.time() + duration

    def get(self, key):
        if not key in self.storage:
            return None

        if not key in self.storage_timeouts:
            return None

        if time.time() - self.storage_timeouts[key] > 0:
            # Invalidate cache
            self.storage_timeouts[key] = 0
            return None

        return self.storage[key]
