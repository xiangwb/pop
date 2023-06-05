from flask import request, jsonify
from flask_restful import Resource
from mongoengine.errors import NotUniqueError,ValidationError as MongoValidationError
from flask_jwt_extended import  jwt_required, get_jwt_identity
from marshmallow import  ValidationError
import pysnooper

from commons.response import format_response
from apps.user.model import User, Role, Permission
from apps.user.schema import EmailUserSchema,RoleSchema, UserProflieCreateSchema,UserProflieSchema,UserProflieListSchema

class RegisterUser(Resource):
    def post(self):
        try:
            user_data = EmailUserSchema().load(request.json)
        except ValidationError as e:
            # return {'message': str(e)}, 400
            return format_response('',str(e),400)
        try:
            user = User(**user_data)
            user.set_password(user_data.get('password'))
            user.save()
        except NotUniqueError as e:
            return format_response('','user exists',400)
        except:
            return format_response('','database error',400)

        # return {'message': 'User registered successfully'}, 201
        return format_response('','User registered successfully',201)
    

class UserById(Resource):
    @jwt_required()
    def get(self,user_id):
        try:
            # user_id = get_jwt_identity()
            user = User.objects(id=user_id).first()
            # return jsonify(user), 200
            schema = UserProflieSchema()
            data = schema.dump(user)
            return format_response(data,'Get user infomation successfully',200)
        except:
            return format_response('','server error',500)


    @jwt_required()
    def put(self,user_id):
        try:
            # user_id = get_jwt_identity()
            user = User.objects(id=user_id).first()

            try:
                user_data = UserProflieSchema().load(request.json)
            except ValidationError as e:
                # return {'message': str(e)}, 400
                return format_response('',str(e),400)

            user.update(**user_data)
            # user.hash_password(user_data['password'])
            user.save()

            # return {'message': 'User profile updated successfully'}, 200
            return format_response('','User profile updated successfully',200)
        except MongoValidationError as e:
            format_response('',str(e),400)
        except:
            return format_response('','server error',500)

class ChangePassword(Resource):
    @jwt_required()
    def post(self,user_id):
        # user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()

        if not user:
            return format_response('','Invalid user_id',401)

        try:
            data = request.json
        except ValidationError as e:
            # return {'message': str(e)}, 400
            return format_response('',str(e),400)

        old_password = data.pop('old_password')
        if  not user.check_password(old_password):
            # return {'message': 'Invalid username or password'}, 401
            return format_response('','Invalid  password',401)

        new_password = data.pop('new_password')
        repeat_new_password = data.pop('repeat_new_password')
        if new_password != repeat_new_password:
            return format_response('',"password doesn't match",400)

        user.set_password(new_password)
        # user.hash_password(user_data['password'])
        user.update(password=user.password)

        # return {'message': 'User profile updated successfully'}, 200
        return format_response('','password updated successfully',200)
    
class UserList(Resource):
    @jwt_required()
    def get(self):
        user = User.objects.all()
        # return jsonify(user), 200
        schema = UserProflieListSchema(many=True)
        data = schema.dump(user)
        return format_response(data,'Get user List successfully',200)
    
    @jwt_required()
    @pysnooper.snoop()
    def post(self):
        try:
            user_data = UserProflieCreateSchema().load(request.json)
            password=user_data.pop('password')
            repeat_password=user_data.pop('repeat_password')
            if password!=repeat_password:
                return format_response("password didn't match",'两次输入的密码不一致',400)
            user = User(**user_data)
            user.set_password(password=password)
            user.save()
        except NotUniqueError as e:
            return format_response('','user exists',400)
        except:
            return format_response('','database error',400)

        # return {'message': 'User registered successfully'}, 201
        return format_response('','User add successfully',201)



class UserRecords(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        return jsonify(user.records), 200

class UserFavorites(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        return jsonify(user.favorites), 200

class Roles(Resource):
    def get(self):
        roles = Role.objects.all()
        return jsonify(roles), 200

    def post(self):
        try:
            role_data = RoleSchema().load(request.json)
        except ValidationError as e:
            return {'message': str(e)}, 400

        permissions = []
        for name in role_data['permissions']:
            permission = Permission.objects(name=name).first()
            if not permission:
                permission = Permission(name=name)
                permission.save()
            permissions.append(permission)

        role = Role(name=role_data['name'], permissions=permissions)
        role.save()

        return {'message': 'Role created successfully'}, 201

class RoleById(Resource):
    def delete(self, role_id):
        role = Role.objects(id=role_id).first()
        if not role:
            return {'message': 'Role not found'}, 404

        role.delete()
        return {'message': 'Role deleted successfully'}, 200

    def put(self, role_id):
        role = Role.objects(id=role_id).first()
        if not role:
            return {'message': 'Role not found'}, 404
        try:
            role_data = RoleSchema().load(request.json)
        except [ValidationError] as e:
            return {'message': str(e)}, 400

        permissions = []
        for name in role_data['permissions']:
            permission = Permission.objects(name=name).first()
            if not permission:
                permission = Permission(name=name)
                permission.save()
            permissions.append(permission)

        role.name = role_data['name']
        role.permissions = permissions
        role.save()

        return {'message': 'Role updated successfully'}, 200