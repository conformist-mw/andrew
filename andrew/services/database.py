import os
from tinydb import TinyDB


class Database(object):
    def __init__(self, andrew):
        self.andrew = andrew
        self.cache = {}

    def __getitem__(self, item):
        if item in self.cache:
            return self.cache[item]
        db = TinyDB(os.path.join(self.andrew.config['STORAGE_PATH'], '{}.json'.format(item)))
        self.cache[item] = db
        return db
help