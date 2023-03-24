from flask import json

from api import create_app
from models import Course, User

app = create_app('config.TestConfig')

def setup_module(module):
    Course.objects.delete()
    User.objects.delete()

def test_create_course():
    response = app.test_client().post('/api/courses', json={
        'name': 'Math'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Math'

def test_create_course_duplicate_name():
    course = Course(name='Math')
    course.save()

    response = app.test_client().post('/api/courses', json={
        'name': 'Math'
    })
    assert response.status_code == 409
    assert response.json['message'] == 'Course already exists'

def test_get_all_courses():
    course1 = Course(name='Math')
    course2 = Course(name='Science')
    course1.save()
    course2.save()

    response = app.test_client().get('/api/courses')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'Math'
    assert response.json[1]['name'] == 'Science'

def test_create_user():
    response = app.test_client().post('/api/users', json={
        'username': 'user1',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'user1'

def test_create_user_duplicate_username():
    user = User(username='user1', password='password123')
    user.save()

    response = app.test_client().post('/api/users', json={
        'username': 'user1',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.json['message'] == 'Username already exists'