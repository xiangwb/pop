from .base import Config

class TestConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test_db',
        'host': 'localhost',
        'port': 27017
    }
    JWT_SECRET_KEY = 'test_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600