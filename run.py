from flask import Flask
from flask_cors import CORS

import os
import sys

from extensions import db, jwt

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import Config
from apps.user.blueprint import user_blueprint
from apps.course.blueprint import course_blueprint
from apps.Carousel.blueprint import carousel_blueprint
from commons.handler import error_handler,log_request_info


# 打开隐藏文件
with open('.env', 'r') as f:
    # 逐行读取文件内容
    for line in f:
        # 忽略以 # 开头的注释行
        if not line.startswith('#'):
            # 按照等号分隔键值对
            key, value = line.strip().split('=', 1)
            # 设置系统环境变量
            os.environ[key] = value



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    jwt.init_app(app)
    app.before_request(log_request_info)
    cors = CORS(app,always_send=True,resources={r"*": {"origins": "*"}})

    error_handler(app)
    
    app.register_blueprint(user_blueprint,url_prefix='/api/v1/users')
    app.register_blueprint(course_blueprint,url_prefix='/api/v1/courses')
    app.register_blueprint(carousel_blueprint,url_prefix='/api/v1/carousels')
    # app.register_blueprint(user_bp)
    # 注册自定义错误
     
   

    print(app.url_map)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()