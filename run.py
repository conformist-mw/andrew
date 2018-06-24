import os
from andrew import AndrewBot

config_file = os.environ.get('ANDREW_BOT_CONFIG', 'local_config.LocalConfig')
print('Start using {}'.format(config_file))

andrew_bot = AndrewBot()
andrew_bot.config.apply(config_file)
andrew_bot.run()
