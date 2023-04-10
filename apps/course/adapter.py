import requests
from .model import SubjectCategory
from apps.user.model import User


def get_user(user_id: str) -> User or None:
    user = User.objects(id=user_id).first()
    return user


def get_parent_category_name(parent_id):
    if parent_id:
        parent = SubjectCategory.objects.get(id=parent_id)
        parent_name = parent.name
    else:
        parent_name = ''
    return parent_name
