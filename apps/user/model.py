from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

from extensions import db

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    nickname = db.StringField(required=True)
    avatar = db.StringField()
    gender = db.StringField(choices=['male', 'female', 'other'])
    birthday = db.DateTimeField()
    email=db.StringField()
    phone=db.StringField()
    created_at = db.DateTimeField(default=datetime.utcnow())

    
    meta = {
        'indexes': ['username'],
        'ordering': ['-created_at']
    }
    

    # def save(self, *args, **kwargs):
    #     self.password = generate_password_hash(self.password)
    #     super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username
        }
    

class Permission(db.EmbeddedDocument):
    name = db.StringField(required=True)
    description = db.StringField()
    action = db.StringField(choices=['create', 'read', 'update', 'delete'], required=True)


class Role(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField()
    permissions = db.ListField(db.EmbeddedDocumentField(Permission))
    created_at = db.DateTimeField(default=datetime.utcnow())
    
    meta = {
        'indexes': ['name'],
        'ordering': ['-created_at']
    }