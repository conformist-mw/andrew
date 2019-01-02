class Sender:

    def __init__(self):
        self.raw = None

    def is_bot(self):
        return self.raw['is_bot']

    def get_id(self):
        return self.raw['id']

    def get_nickname(self):
        nickname = self.raw['first_name'] if 'first_name' in self.raw else ''
        nickname += ' {}'.format(self.raw['last_name']) if 'last_name' in self.raw else ''
        return nickname

    def is_moder(self):
        return False

    def is_admin(self):
        return False

    @staticmethod
    def build_from_raw(raw):
        sender = Sender()

        sender.raw = raw
        return sender
