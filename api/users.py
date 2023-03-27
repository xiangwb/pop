from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask import Blueprint

# from . import api_bp
from models.user import User

user_bp = Blueprint('user', __name__,url_prefix="/users")

@user_bp.route('/users', methods=['GET'])
@jwt_required
def get_users():
    users = User.objects().exclude('password')
    return jsonify(users), 200

@user_bp.route('/users/<string:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    user = User.objects(id=user_id).exclude('password').first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    if User.objects(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    user = User(username=username, password=password)
    user.save()
    return jsonify(user), 201

@user_bp.route('/users/<string:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username:
        user.username = username
    if password:
        user.password = password
    user.save()
    return jsonify(user), 200

@user_bp.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user.delete()
    return '', 204