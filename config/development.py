from .base import Config

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'dev_db',
        'host': 'localhost',
        'port': 27017
    }