import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGODB_DB','pop'),
        'host': os.environ.get('MONGODB_HOST', 'mongo'),
        'port': int(os.environ.get('MONGODB_PORT', '27017')),
        'username': os.environ.get('MONGODB_USERNAME', 'root'),
        'password': os.environ.get('MONGODB_PASSWORD', '1qaz0plm'),
        'authentication_source': os.environ.get('MONGODB_AUTH_SOURCE', 'admin'),
        'authentication_mechanism': os.environ.get('MONGODB_AUTH_MECHANISM', 'SCRAM-SHA-256')
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    API2D_API_KEY=os.environ.get('API2D_API_KEY','default')
 