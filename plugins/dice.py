from random import randint
import re
from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Отвечает за разбор дайсов вида 1д6'

    def is_visible(self):
        return True

    async def filter_handler(self, message):
        p = re.compile('^(\d+)[дd](\d+)$', re.IGNORECASE)
        m = p.match(message.text)
        count, val = m.groups()

        string = '{}д{}: '.format(count, val)

        for i in range(int(count)):
            string += '\[{}] '.format(randint(1, int(val)))

        await message.send_back(string)
