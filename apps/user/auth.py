from flask import request
from flask_restful import Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from marshmallow import  ValidationError
import pysnooper

from commons.response import format_response
from .model import User
from .schema import LoginSchema



class LoginUser(Resource):
    @pysnooper.snoop(depth=2)
    def post(self):
        try:
            user_data = LoginSchema().load(request.json)
        except ValidationError as e:
            # return {'message': str(e)}, 400
            return format_response(str(e),'parameter error',400)

        user = User.objects(username=user_data['username']).first()
        if not user or not user.check_password(user_data['password']):
            # return {'message': 'Invalid username or password'}, 401
            return format_response('','Invalid username or password',401)

        access_token = create_access_token(identity=str(user.id))
        # return {'access_token': access_token}, 200
        return format_response({'access_token': access_token,'id':str(user.id)},'login success',200)

class LogoutUser(Resource):
    @jwt_required()
    def post(self):
        # return {'message': 'User logged out successfully'}, 200
        return format_response('','User logged out successfully',200)