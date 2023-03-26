from flask import jsonify

def unauthorized(message):
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = 401
    return response


def bad_request(message):
    response = jsonify({"error": "bad_request", "message": message})
    response.status_code = 400
    return response