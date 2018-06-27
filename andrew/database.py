from tinydb import TinyDB, Storage


class Database(object):
    def __init__(self, andrew):
        self.andrew = andrew

    def __getitem__(self, item):
        db = TinyDB(self.andrew.config['STORAGE_PATH'])
        table = db.table(item)
        return table
