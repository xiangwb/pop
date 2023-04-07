from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)