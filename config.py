import configparser


class BotConfig:
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['app']['token']
    db_url = config['database']['url']