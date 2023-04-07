from flask import request
from flask_restful import Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from models.user import User
from apps.user.schema.auth.auth import LoginSchema

from marshmallow import  ValidationError

class LoginUser(Resource):
    def post(self):
        try:
            user_data = LoginSchema().load(request.json)
        except ValidationError as e:
            return {'message': str(e)}, 400

        user = User.objects(email=user_data['email']).first()
        if not user or not user.verify_password(user_data['password']):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=str(user.id))
        return {'access_token': access_token}, 200

class LogoutUser(Resource):
    @jwt_required()
    def post(self):
        return {'message': 'User logged out successfully'}, 200