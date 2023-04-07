from flask import Flask

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.user.resource import user_blueprint
from config import Config
from extensions import db, jwt



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_blueprint)
    # app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()