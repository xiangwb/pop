from flask import Blueprint

from flask_restful import Api

from resource.user import RegisterUser,UserPassword
from resource.auth import LoginUser,LogoutUser

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

api.add_resource(LoginUser,'/login')
api.add_resource(LogoutUser,'logout')
api.add_resource(RegisterUser,'/register')
api.add_resource(UserPassword,'/<:id>/update_password')