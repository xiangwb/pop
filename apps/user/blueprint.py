from flask import Blueprint

from flask_restful import Api

from apps.user.resource import RegisterUser,UserPassword
from apps.user.auth import LoginUser,LogoutUser

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

api.add_resource(LoginUser,'/login/')
api.add_resource(LogoutUser,'/logout/')
api.add_resource(RegisterUser,'/register/')
api.add_resource(UserPassword,'/<string:id>/update_password/')