import pysnooper
from flask import request
from .response import format_response
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def not_found(error):
    return format_response('','Not found', 404)

def internal_server_error(error):
    return format_response('','internal server error', 500)

def error_handler(app):
   app.register_error_handler(404,not_found)
   app.register_error_handler(500,internal_server_error)
    




# @pysnooper.snoop()
def log_request_info():
    logger.debug('Request Headers:%s', request.headers)
    logger.debug('Request Method:%s', request.method)
    logger.debug('Request URL:%s', request.url)
    logger.debug('Request Data:%s', request.data)
    logger.debug('Request Args:%s', request.args)
    logger.debug('Request Form:%s', request.form)
    logger.debug('Request Files:%s', request.files)

    
    