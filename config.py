from configparser import ConfigParser


config = ConfigParser()
config.read('config_buffet.ini')

config_api = config['api']

API_URL = config_api['api_url']
