from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .auth import *
from .users import *
# from .courses import *