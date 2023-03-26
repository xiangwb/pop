from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from models.user import User
from utils.errors import unauthorized, bad_request

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return bad_request("Missing username or password")

    user = User.get_by_username(username)

    if user is None or not user.check_password(password):
        return unauthorized("Invalid username or password")

    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token)