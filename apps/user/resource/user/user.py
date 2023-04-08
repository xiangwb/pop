from flask import request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError

from models import User, Role, Permission
from apps.user.schema.user.user import UserSchema,RoleSchema

class RegisterUser(Resource):
    def post(self):
        try:
            user_data = UserSchema().load(request.json)
        except ValidationError as e:
            return {'message': str(e)}, 400

        user = User(**user_data)
        user.hash_password()
        user.save()

        return {'message': 'User registered successfully'}, 201
    

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        return jsonify(user), 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()

        try:
            user_data = UserSchema().load(request.json)
        except ValidationError as e:
            return {'message': str(e)}, 400

        user.email = user_data['email']
        user.hash_password(user_data['password'])
        user.save()

        return {'message': 'User profile updated successfully'}, 200

class UserPassword(Resource):
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()

        try:
            user_data = UserSchema().load(request.json)
        except ValidationError as e:
            return {'message': str(e)}, 400

        user.hash_password(user_data['password'])
        user.save()

        return {'message': 'User password updated successfully'}, 200

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