from .base import Config

class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'prod_db',
        'host': 'mongodb://mongo:27017',
        'username': 'prod_user',
        'password': 'prod_password',
        'authSource': 'admin',
        'authMechanism': 'SCRAM-SHA-256'
    }
    JWT_SECRET_KEY = 'prod_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600