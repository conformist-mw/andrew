import random
import re
from andrew.api.plugin import AbstractPlugin


class Plugin(AbstractPlugin):
    def __init__(self, andrew):
        self.andrew = andrew

    def register(self):
        self.andrew.filters.add_filter(self.filter_handler)

    def get_description(self):
        return 'Реакция на разные слова в сообщениях'

    def is_visible(self):
        return True

    async def filter_handler(self, message):
        m = re.search("2007(?:[мй]|ого|ому|)", message.text)
        if m is not None:
            await message.send_back(random.choice([
                "Никто и никогда не вернет 2007-й год",
                "Сентяяябрь гориит",
                "За что теперь тебя любить?",
                "Зачем я должен верить в тебя?",
                "...осколками наших разбитых сердец",
                "Мы с тобой вулканы",
                "Это просто дождь",
                "Я плаачу и вместе с тем умираю",
                "Остальное забыл навсегда",
                "Поцелуй из огня!"
            ]))

        m = re.search("(добро[гое] |всем |)утр[ао]( всем|)", message.text)
        if m is not None:
            await message.send_back(random.choice([
                "И тебе доброе утро!",
                "Добрейшего тебе утра!",
                "Какое утро?! Солнце уже высоко!"
            ]))

        m = re.search("(доброй |всем |спокойной |)(ночк?и|[сш]пать)( всем|)", message.text)
        if m is not None:
            await message.send_back(random.choice([
                "Сладких снов!",
                "Доброчи!",
                "Нежной ночечки!",
                "Крепко спатушки!"
            ]))

        m = re.search("(всем |)(здарова?|приве?т?)( всем|)", message.text)
        if m is not None:
            await message.send_back(random.choice([
                "Привет, привет!",
                "Хаюшки!",
                "Приветствую тебя!",
                "Низкий Вам поклон!"
            ]))

        m = re.search("пыщ[ь]?([ ]?пыщ|)", message.text)
        if m is not None:
            await message.send_back("Пыщь-пыщь, ололо, я -- водитель НЛО!")
