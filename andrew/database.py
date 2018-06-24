from tinydb import TinyDB, Storage


class Database(object):
    def __init__(self, vk_bot):
        self.vk_bot = vk_bot

    def __getitem__(self, item):
        db = TinyDB(self.vk_bot.config['STORAGE_PATH'])
        table = db.table(item)
        return table
