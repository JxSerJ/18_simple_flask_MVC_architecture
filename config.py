# Это файл конфигурации приложения, здесь может храниться путь к бд, ключ шифрования, что-то еще.


from constants import DATABASE_PATH


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 4}
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
