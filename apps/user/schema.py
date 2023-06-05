from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    type = fields.String(required=True)
    autoLogin = fields.Boolean(required=True)

class EmailUserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True,load_only=True, validate=validate.Length(min=6, max=50))
    nickname = fields.String(required=True, validate=validate.Length(min=6, max=50))

class UserProflieSchema(Schema):
    id = fields.String(dump_only=True)
    # username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    username = fields.String(required=True, unique=True)
    # password = fields.String(required=True)
    nickname = fields.String(required=True)
    avatar = fields.String()
    gender = fields.String(choices=['male', 'female', 'other'],required=True)
    birthday = fields.DateTime()
    email=fields.String(required=True)
    phone=fields.String(required=True)

class UserProflieListSchema(Schema):
    id =fields.String(dump_only=True)
    username = fields.String(required=True, unique=True)
    # password = fields.String(required=True)
    nickname = fields.String(required=True)
    avatar = fields.String()
    gender = fields.String(choices=['male', 'female', 'other'])
    birthday = fields.DateTime()
    email=fields.String()
    phone=fields.String()
    created_at = fields.DateTime(ump_only=True)

class UserProflieCreateSchema(Schema):
    id =fields.String(dump_only=True)
    username = fields.String(required=True, unique=True)
    # password = fields.String(required=True)
    nickname = fields.String(required=True)
    avatar = fields.String()
    gender = fields.String(choices=['male', 'female', 'other'],required=True)
    birthday = fields.DateTime()
    email=fields.String(required=True)
    phone=fields.String(required=True)
    password=fields.String(required=True)
    repeat_password=fields.String(required=True)
   



class RoleSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    permissions = fields.List(fields.Nested('PermissionSchema'))


class PermissionSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    resource = fields.String(required=True)
    actions = fields.List(fields.String(validate=validate.OneOf(['read', 'write'])))