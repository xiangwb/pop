from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from commons.logger import Logger
from flask_caching import Cache
from commons.apispec import APISpecExt
from commons.response import format_response

db = MongoEngine()
jwt = JWTManager()
logger = Logger()
apispec = APISpecExt()
cache = Cache()


@jwt.revoked_token_loader
def handle_revoked_token():
    return format_response('',{'msg': 'Token has been revoked'},401)


@jwt.expired_token_loader
def handle_expired_token():
    return format_response('',{'msg': 'Token has expired'},401)


@jwt.invalid_token_loader
def handle_invalid_token():
    return format_response('',{'msg': 'Invalid token'}, 401)

@jwt.unauthorized_loader
def handle_no_auth_error(error):
    return format_response('','Missing Authorization Header',401)



