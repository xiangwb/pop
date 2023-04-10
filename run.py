from flask import Flask

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.user.blueprint import user_blueprint
from apps.course.blueprint import course_blueprint
from config import Config
from extensions import db, jwt



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_blueprint,url_prefix='/api/v1/users')
    app.register_blueprint(course_blueprint,url_prefix='/api/v1/courses')
    # app.register_blueprint(user_bp)

    print(app.url_map)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()