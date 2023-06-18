from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
database = config['Database']
USER = database['USER']
PASSWORD = database['PASSWORD']
HOST = database['HOST']
PORT = database['PORT']
DATABASE = database['DATABASE']
