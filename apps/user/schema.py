from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=50))
    email = fields.Email(required=True)
    nickname = fields.String(required=True, validate=validate.Length(min=6, max=50))


class RoleSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    permissions = fields.List(fields.Nested('PermissionSchema'))


class PermissionSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    resource = fields.String(required=True)
    actions = fields.List(fields.String(validate=validate.OneOf(['read', 'write'])))