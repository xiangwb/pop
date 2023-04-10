from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from commons.logger import Logger
from flask_caching import Cache
from commons.apispec import APISpecExt

db = MongoEngine()
jwt = JWTManager()
logger = Logger()
apispec = APISpecExt()
cache = Cache()