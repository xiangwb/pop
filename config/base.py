import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGODB_DB','default'),
        'MONGODB_HOST': os.environ.get('MONGODB_HOST', 'localhost'),
        'MONGODB_PORT': int(os.environ.get('MONGODB_PORT', '27117')),
        'MONGODB_USERNAME': os.environ.get('MONGODB_USERNAME', ''),
        'MONGODB_PASSWORD': os.environ.get('MONGODB_PASSWORD', ''),
        'MONGODB_AUTH_SOURCE': os.environ.get('MONGODB_AUTH_SOURCE', 'admin'),
        'MONGODB_AUTH_MECHANISM': os.environ.get('MONGODB_AUTH_MECHANISM', 'SCRAM-SHA-256')
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))