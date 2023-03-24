
from werkzeug.security import generate_password_hash,check_password_hash

from extensions import db

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def save(self, *args, **kwargs):
        self.password = generate_password_hash(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username
        }