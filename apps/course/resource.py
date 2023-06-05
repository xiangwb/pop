import json
import marshmallow
import mongoengine
import pysnooper
from flask import request
from flask_restful import Resource
from flask_jwt_extended import  jwt_required, get_jwt_identity
import mongoengine as mg
import requests

from apps.course.utils import get_next_item_id
from commons.pagination import Pagination
from extensions import logger
from apps.course.model import SubjectCategory, Subject, Point, Item, PointRelation
from apps.course.schema import SubjectCategorySchema, SubjectSchema, ItemSchema, PointSchema, PointRelationSchema, \
    StudyItemSchema
from commons.response import format_response
from apps.course.adapter import get_parent_category_name, get_user
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class SubjectCategoryResource(Resource):
    """
    课程分类查改删
    """
    @jwt_required()
    def get(self, _id):
        schema = SubjectCategorySchema()
        try:
            subject_category = SubjectCategory.objects.get(id=_id)
            parent_id = subject_category.parent_id
            parent_name = get_parent_category_name(parent_id)
            subject_category.parent_name = parent_name
            return format_response(schema.dump(subject_category), "get subject category detail success", 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject category is not exist', 404)
    @jwt_required()
    def put(self, _id):
        schema = SubjectCategorySchema()
        try:
            subject_category = SubjectCategory.objects.get(id=_id)
            data = schema.load(request.json)
            subject_category.update(**data)
            subject_category.reload()
            parent_id = subject_category.parent_id
            parent_name = get_parent_category_name(parent_id)
            subject_category.parent_name = parent_name
            return format_response(schema.dump(subject_category), 'subject category updated', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject category is not exist', 404)

    def delete(self, _id):
        try:
            SubjectCategory.objects.get(id=_id).delete()
            # 删除相关联对象
            SubjectCategory.objects(parent_id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'subject category deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject category is not exist', 404)


class SubjectCategoryListResource(Resource):
    """
    课程分类创建与列表
    """
    @jwt_required()
    def get(self):
        try:
            schema = SubjectCategorySchema()
            # child_schema = SubjectCategorySchema(many=True)
            # subject_category_list = SubjectCategory.objects(path='/')
            # resp = []
            # for subject_category_obj in subject_category_list:
            #     path_prefix = '/' + subject_category_obj.name
            #     child_subject_list = SubjectCategory.objects(path=path_prefix)
            #     subject_category = schema.dump(subject_category_obj)
            #     subject_category['children'] = child_schema.dump(child_subject_list)
            #     resp.append(subject_category)
            categories = []
            subject_category_list = SubjectCategory.objects.all()
            for category in subject_category_list:
                parent_id = category.parent_id
                parent_name = get_parent_category_name(parent_id)
                category.parent_name = parent_name
                categories.append(category)
            objs, page = Pagination(categories).paginate(schema)
            return format_response(objs, 'get subject category list success', 200)
        except Exception as e:
            return format_response(e.args, 'get subject category list failure', 500)
    @jwt_required()
    def post(self):
        try:
            logger.debug("创建课程分类")
            schema = SubjectCategorySchema()
            data = request.json
            logger.debug("received data:{}".format(data))
            if 'parent_id' in data:
                if data['parent_id'] in ['None', '']:
                    data.pop('parent_id')
            data = schema.load(request.json)
            subject_category = SubjectCategory.objects.create(**data)
            parent_id = subject_category.parent_id
            parent_name = get_parent_category_name(parent_id)
            subject_category.parent_name = parent_name
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            return format_response(schema.dump(subject_category), 'subject category created', 201)
        except mg.errors.NotUniqueError:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response('', 'subject category exists', 400)
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500)


class CategorySubjectResource(Resource):
    """
    查询某个课程分类下的课程
    """

    @pysnooper.snoop()
    @jwt_required()
    def get(self, _id):
        try:
            schema = SubjectSchema()
            subject_list = Subject.objects(category__in=[SubjectCategory.objects.get(id=_id)])
            objs, page = Pagination(subject_list).paginate(schema)
            return format_response(objs, 'get subject list success', 200, page=page), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'get subject list failure', 500), 500


class SubjectResource(Resource):
    """
    课程查改删接口
    """

    def get(self, _id):
        schema = SubjectSchema()
        try:
            subject = Subject.objects.get(id=_id)
            subject.category_names = [SubjectCategory.objects.get(id=category_id).name for category_id in
                                      subject.category_ids]
            return format_response(schema.dump(subject), "get subject detail success", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject is not exist', 404), 404
    @jwt_required()
    def put(self, _id):
        schema = SubjectSchema()
        try:
            subject = Subject.objects.get(id=_id)
            data = schema.load(request.json)
            subject.update(**data)
            subject.reload()
            subject.category_names = [SubjectCategory.objects.get(id=category_id).name for category_id in
                                      subject.category_ids]
            return format_response(schema.dump(subject), "subject updated", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject is not exist', 404), 404
    @jwt_required()
    def delete(self, _id):
        try:
            Subject.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'subject  deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject is not exist', 404)


class SubjectListResource(Resource):
    """
    课程列表和创建
    """
    
    def get(self):
        try:
            schema = SubjectSchema(many=True)
            subjects = Subject.objects.all()
            subject_list = []
            for subject in subjects:
                subject.category_names = [SubjectCategory.objects.get(id=category_id).name for category_id in
                                          subject.category_ids]
                subject_list.append(subject)
            objs, page = Pagination(subject_list).paginate(schema)
            return format_response(objs, 'get subject list success', 200, page=page), 200
        except Exception as e:
            return format_response(e.args, 'get subject list failure', 500), 500

    
    @jwt_required()
    @pysnooper.snoop()
    def post(self):
        try:
            schema = SubjectSchema()
            headers = request.headers
            logger.info(headers)
            data = schema.load(request.json)
            user_id = get_jwt_identity()
            data['creator_id'] = user_id
            subject = Subject.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            subject.category_names = [SubjectCategory.objects.get(id=category_id).name for category_id in
                                      subject.category_ids]
            return format_response(schema.dump(subject), 'subject  created', 201), 201
        except marshmallow.exceptions.ValidationError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'subject exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500


class ItemResource(Resource):
    """
    条目查改删接口
    """
    @jwt_required()
    def get(self, _id):
        schema = ItemSchema()
        try:
            item = Item.objects.get(id=_id)
            return format_response(schema.dump(item), "get item detail success", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'item is not exist', 404), 404
    @jwt_required()
    def put(self, _id):
        user_id = get_jwt_identity()
        data = request.json
        data['creator_id']=user_id
        schema = ItemSchema()
        try:
            item = Item.objects.get(id=_id)
            v_data = schema.load(data)
            item.update(**v_data)
            item.reload()
            return format_response(schema.dump(item), "item updated", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'item is not exist', 404), 404
    @jwt_required()
    def delete(self, _id):
        try:
            Item.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'item  deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'item is not exist', 404)


class ItemListResource(Resource):
    """
    条目和创建
    """

    def get(self):
        try:
            schema = ItemSchema(many=True)
            subject_id = request.args.get('subject_id')
            if subject_id:
                item_list=Item.objects(subject_id=subject_id)
            else:
                item_list = Item.objects.all()
            objs, page = Pagination(item_list).paginate(schema)
            return format_response(objs, 'get item list success', 200, page=page), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return format_response(e.args, 'get item list failure', 500), 500

    @jwt_required()
    def post(self):
        try:
            schema = ItemSchema()
            user_id = get_jwt_identity()
            data = request.json
            data['creator_id']=user_id
            creator = get_user(user_id)
            data = schema.load(request.json)  
            item = Item.objects.create(**data)        
            # point_id = data.get('point_id')
            # point = Point.objects.get(id=point_id)
            # item.point_name = point.name
            # related_point_ids = data.get('related_point_ids')
            # related_point_names = []
            # if related_point_ids:
            #     for related_point_id in related_point_ids:
            #         related_point = Point.objects.get(id=related_point_id)
            #         related_point_name = related_point.name
            #         related_point_names.append(related_point_name)
            # item.related_point_names = related_point_names
            # subject_id = data.get('subject_id')
            # subject = Subject.objects.get(id=subject_id)
            # subject_name = subject.name
            # item.subject_name = subject_name
            # item.creator_name = creator.username
            
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            # subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(item), 'item  created', 201), 201
        except (marshmallow.exceptions.ValidationError, mongoengine.errors.ValidationError) as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'item exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500


class PointListResource(Resource):
    """
    课程知识点的创建和列表
    """

   
    @jwt_required()
    @pysnooper.snoop()
    def get(self):
        try:
            schema = PointSchema(many=True)
            subject_id = request.args.get('subject_id')
            # if not subject_id:
            #     return format_response('parameter subject_id missing', 'get point list failure', 400)
            if subject_id:
                point_list = Point.objects(subject_id=subject_id)
            else:
                point_list = Point.objects.all()
            points = []
            for point in point_list:
                subject_name = Subject.objects.get(id=point.subject_id).name
                point.subject_name = subject_name
                points.append(point)
            objs, page = Pagination(points).paginate(schema)
            return format_response(objs, 'get point list success', 200, page=page), 200
        except Exception as e:
            return format_response(e.args, 'get point list failure', 500), 500
    @jwt_required()
    def post(self):
        try:
            schema = PointSchema()
            data = schema.load(request.json)
            item = Point.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            # subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(item), 'point  created', 201), 201
        except (marshmallow.exceptions.ValidationError, mongoengine.errors.ValidationError) as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'point in the subject exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500
        

class PointResource(Resource):
    """
    课程查改删接口
    """
    @jwt_required()
    def get(self, _id):
        schema = PointSchema()
        try:
            point = Point.objects.get(id=_id)
            return format_response(schema.dump(point), "get point detail success", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'point is not exist', 404), 404
    @jwt_required()
    def put(self, _id):
        schema = PointSchema()
        try:
            point = Point.objects.get(id=_id)
            data = schema.load(request.json)
            point.update(**data)
            point.reload()
            return format_response(schema.dump(point), "point updated", 200), 200
        except (marshmallow.exceptions.ValidationError, mongoengine.errors.ValidationError) as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'point in the subject exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500
        
    @jwt_required()
    def delete(self, _id):
        try:
            Point.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'point  deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'point is not exist', 404)



class PointRelationResource(Resource):
    """
    知识图谱的获取、修改
    """

    @jwt_required()
    def get(self, _id):
        try:
            schema = PointRelationSchema()
            relation = PointRelation.objects.get(id=_id)
            return format_response(schema.dump(relation), "get point relation detail success", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'point relation is not exist', 404), 404
    
    @jwt_required()
    def put(self, _id):
        schema = PointRelationSchema()
        try:
            relation = PointRelation.objects.get(id=_id)
            data = schema.load(request.json)
            relation.update(**data)
            relation.reload()
            return format_response(schema.dump(relation), "point relation updated", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'relation point is not exist', 404), 404
    
    @jwt_required() 
    @pysnooper.snoop()   
    def delete(self,_id):
        try:
            PointRelation.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'point  deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'point is not exist', 404)

class PointRelationListResource(Resource):
    """
    知识图谱的创建
    """
    @jwt_required()
    def post(self):
        try:
            schema = PointRelationSchema()
            data = schema.load(request.json)
            item = PointRelation.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            # subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(item), 'point relation created', 201), 201
        except (marshmallow.exceptions.ValidationError, mongoengine.errors.ValidationError) as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'point relation exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500

    @jwt_required()
    def get(self):
        def get_type_display(_type):
            if _type=='subject':
                return '课程'
            else:
                return '知识点'
            
        def get_relation_display(relation):
            if relation=='contains':
                return '包含'
            else:
                return '需要定义'
        try:
            schema = PointRelationSchema(many=True)
            subject_id = request.args.get('subject_id')
            if subject_id:
                point_relations = PointRelation.objects(subject_id=subject_id)
            else:
                point_relations = PointRelation.objects.all()
            point_relation_list = []
            for point_relation in point_relations:
                from_node_id = point_relation.from_node_id
                from_node_type = point_relation.from_node_type
                to_node_id = point_relation.to_node_id
                to_node_type = point_relation.to_node_type
                subject = Subject.objects.get(id=point_relation.subject_id)
                subject_name = subject.name
                if from_node_type == 'subject':
                    from_node_type_display = '课程'
                    
                    from_node_name = subject_name
                else:
                    from_node_type_display = '知识点'
                    from_node = Point.objects.get(id=from_node_id)
                    from_node_name = from_node.name
                to_node = Point.objects.get(id=to_node_id)
                to_node_name = to_node.name
                point_relation.subject_name = subject_name
                point_relation.from_node_type_display = from_node_type_display
                point_relation.to_node_type_display = get_type_display(to_node_type)
                point_relation.relation_display = get_relation_display(point_relation.relation)
                point_relation.from_node_name = from_node_name
                point_relation.to_node_name = to_node_name
                point_relation_list.append(point_relation)
            objs, page = Pagination(point_relation_list).paginate(schema)
            return format_response(objs, 'get point relation list success', 200, page=page), 200
        except Exception as e:
            return format_response(e.args, 'get point list failure', 500), 500


class PointRelationGraphResource(Resource):
    """
    知识图谱
    """
    @jwt_required()
    @pysnooper.snoop(max_variable_length=5000)
    def get(self):
        try:
            subject_id = request.args.get('subject_id')
            if not subject_id:
                return format_response("subject_id not provided or null", 'param error', 400), 400
            subject = Subject.objects.get(id=subject_id)
            subject_name = subject.name
            graph = dict()
            graph['rootId'] = subject_id
            # point_schema = PointSchema(many=True)
            points = Point.objects(subject_id=subject_id)
            point_list = []
            root_node = {'id': subject_id, 'text': subject_name, 'color': '#ff8c00'}
            point_list.append(root_node)
            for point in points:
                point_dict = dict()
                point_dict['id'] = str(point.id)
                point_dict['text'] = point.name
                point_dict['color'] = '#43a2f1'
                point_list.append(point_dict)
            graph['nodes'] = point_list
            # relation_schema = PointRelationSchema(many=True)
            point_relations = PointRelation.objects(subject_id=subject_id)
            point_relation_list = []
            for point_relation in point_relations:
                relation_dict = dict()
                from_node_id = point_relation.from_node_id
                # from_node_type = point_relation.from_node_type
                to_node_id = point_relation.to_node_id
                # to_node_type = point_relation.to_node_type
                # if from_node_type == 'subject':
                #     # from_node = subject
                #     from_node_name = subject_name
                # else:
                #     from_node = Point.objects.get(id=from_node_id)
                #     from_node_name = from_node.name
                # to_node = Point.objects.get(id=to_node_id)
                # to_node_name = to_node.name
                relation_dict['id'] = point_relation.to_node_id
                relation_dict['from'] = from_node_id
                relation_dict['to'] = to_node_id
                relation_dict['text'] = point_relation.relation
                point_relation_list.append(relation_dict)
            graph['lines'] = point_relation_list
            return format_response(graph, 'get point graph  success', 200), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            return format_response(e.args, 'get point graph failure', 500), 500



class ItemGetterResource(Resource):
    """
    获取下一条需要学习的条目
    """
    @jwt_required()
    @pysnooper.snoop()
    def post(self):
        try:
            schema = StudyItemSchema()
            data = request.json
            user_id = get_jwt_identity()
            if not user_id:
                return format_response("no response header X-Auth-User-Id", 'server error', 500), 500
            item_id = data.get('item_id')
            # item = Item.objects.get(id=item_id)
            subject_id = data.get('subject_id')
            # subject = Subject.objects.get(id=subject_id)
            try:
                if item_id:
                    answer = data.get('answer')
                    if not subject_id:
                        item = Item.objects.get(id=item_id)
                        if not item:
                            return format_response("item_id is error", 'param error', 400), 400
                        subject_id = item.subject_id
                    next_item_id, status = get_next_item_id(user_id=user_id, subject_id=subject_id, item_id=item_id,
                                                            answer=answer)
                else:
                    if not subject_id:
                        return format_response("subject_id is missing", 'param error', 400), 400
                    next_item_id, status = get_next_item_id(user_id=user_id, subject_id=subject_id, item_id=None,
                                                            answer=None)
                if status:
                    return format_response('subject complete', "subject complete", 200), 200
            except Exception:
                return format_response("获取条目错误", 'server error', 500), 500
            next_item = Item.objects.get(id=next_item_id)
            return format_response(schema.dump(next_item), "get item detail success", 200), 200

        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500


class ChatResource(Resource):
    @jwt_required()
    @pysnooper.snoop(max_variable_length=2000)
    def post(self):
        # Get the request data
        from config.base import Config
        data = request.get_json()

      # 将用户输入发送到ChatGPT模型进行处理
        response = requests.post(
            "https://openai.api2d.net/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                "Authorization": f"Bearer {Config.API2D_API_KEY}"
            },
            json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": data['prompt']
                }
            ],
            "safe_mode": False
            }
        ).json()

        # 从模型响应中提取生成的文本响应
        # bot_response = response.json()["choices"][0]["text"].strip()
        # {'id': 'chatcmpl-7NspOlgp81rX9bxShDMjaTMWcsjR4', 'object': 'chat.completion', 'created': 1685926658, 'model': 'gpt-3.5-turbo-0301', 'usage': {'prompt_tokens': 19, 'completion_tokens': 124, 'total_tokens': 143, 'pre_token_count': 4096, 'pre_total': 42, 'adjust_total': 40, 'final_total': 2}, 'choices': [{'message': {'role': 'assistant', 'content': '元类是用于创建类的类。它们是Python中非常高级和高度动态的概念，在大多数情况下并不常见或需要使用。元类的作用是控制对象的创建和行为，与普通类的创建是类似的。元类可以创建新类，也可以修改现有类的行为，包括其方法、属性等。元类可以通过派生自type类来实现，也可以使用元类创建元类。'}, 'finish_reason': 'stop', 'index': 0}], 'cache': 'e4cd8f93124201df4009476d72ea87134ef3021c'}
        if 'choices' not in response or len(response['choices']) == 0:
            return format_response({'error': 'No response from the API.'},'No response from the API',500), 500

        # Return the first choice from the API response
        return format_response({'response': response['choices'][0]['message']['content']},'requests success',200),200