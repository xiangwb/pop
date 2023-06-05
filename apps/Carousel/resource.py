from flask_restful import Resource
from flask_jwt_extended import  jwt_required, get_jwt_identity
import mongoengine as mg
from flask import request
import pysnooper
from apps.Carousel.schema import CarouselSchema
from apps.Carousel.model import Carousel
from commons.response import format_response

class CarouselResource(Resource):
    """
    轮播图查改删
    """
    @jwt_required()
    def get(self, _id):
        schema = CarouselSchema()
        try:
            carousel = Carousel.objects.get(id=_id)
            return format_response(schema.dump(carousel), "get carousel detail success", 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'carousel is not exist', 404)
        
    @jwt_required()
    def put(self, _id):
        schema = CarouselSchema()
        try:
            carousel = Carousel.objects.get(id=_id)
            data = schema.load(request.json)
            carousel.update(**data)
            carousel.reload()
            return format_response(schema.dump(carousel), 'carousel updated', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'carousel is not exist', 404)
        
    @jwt_required()
    def delete(self, _id):
        try:
            Carousel.objects.get(id=_id).delete()
            return format_response('', 'carousel deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'carousel is not exist', 404)


class CarouselListResource(Resource):
    """
    轮播图创建与列表
    """

    @pysnooper.snoop() 
    def get(self):
        try:
            schema = CarouselSchema(many=True)
            caresel_list = Carousel.objects(is_active=True)
      
            return format_response(schema.dump(caresel_list), 'get carousel list success', 200)
        except Exception as e:
            return format_response(e.args, 'get carousel list failure', 500)
    
    @jwt_required()
    def post(self):
        try:
            schema = CarouselSchema()
            data = request.json
            data = schema.load(request.json)
            user_id = get_jwt_identity()
            data['creator_id'] = user_id
            carousel = Carousel.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            return format_response(schema.dump(carousel), 'carousel created', 201)
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            return format_response(e.args, 'server error', 500)