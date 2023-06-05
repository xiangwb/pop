from flask import Blueprint

from flask_restful import Api

from apps.Carousel.resource import CarouselListResource,CarouselResource

carousel_blueprint = Blueprint('carousel', __name__)
api = Api(carousel_blueprint)

api.add_resource(CarouselResource,'/carousels/<string:_id>/')
api.add_resource(CarouselListResource,'/carousels/')
