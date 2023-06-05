from flask import Blueprint

from flask_restful import Api

from apps.user.resource import RegisterUser,ChangePassword,UserById,UserList
from apps.user.auth import LoginUser,LogoutUser

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

api.add_resource(LoginUser,'/login/')
api.add_resource(LogoutUser,'/logout/')
api.add_resource(UserById,'/profile/<string:user_id>/')
api.add_resource(UserList,'/profile/')
api.add_resource(RegisterUser,'/register/')
api.add_resource(ChangePassword,'/<string:user_id>/change_password/')