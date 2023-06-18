from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
BOT_TOKEN = config['Telegram']['BOT_TOKEN']
