from datetime import timedelta

from pop import app
from flask_jwt_extended import JWTManager


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from pop.models.token import Token

    jti = decrypted_token['jti']
    token = Token.objects(jti=jti).first()
    return token is not None


@jwt.revoked_token_loader
def handle_revoked_token():
    return jsonify({'msg': 'Token has been revoked'}), 401


@jwt.expired_token_loader
def handle_expired_token():
    return jsonify({'msg': 'Token has expired'}), 401


@jwt.invalid_token_loader
def handle_invalid_token():
    return jsonify({'msg': 'Invalid token'}), 401


def create_token(user_id):
    from pop.models.token import Token

    access_token = jwt.create_access_token(identity=str(user_id))
    refresh_token = jwt.create_refresh_token(identity=str(user_id))

    token = Token(
        jti=jwt.get_jti(encoded_token=access_token),
        user_id=user_id
    )
    token.save()

    return {'access_token': access_token, 'refresh_token': refresh_token}


def revoke_token(jti):
    from pop.models.token import Token

    token = Token.objects(jti=jti).first()

    if token:
        token.delete()