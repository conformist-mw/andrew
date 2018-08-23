class AbstractSender:
    def __init__(self):
        self.raw = None

    def is_bot(self):
        return False

    def get_id(self):
        return None

    def get_nickname(self):
        return None

    def is_moder(self):
        return False

    def is_admin(self):
        return False
