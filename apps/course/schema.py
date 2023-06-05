import traceback

from marshmallow import Schema, fields
from apps.course.adapter import get_user
from apps.course.model import Point, Subject
from extensions import logger


class SubjectCategorySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    parent_id = fields.String(required=False)
    parent_name = fields.String(required=False, dump_only=True)
    path = fields.String(required=False, dump_only=True)


class SubjectSchema(Schema):
    id = fields.String(dump_only=True)
    creator = fields.Method('get_creator', dump_only=True)
    category_ids = fields.List(fields.String)
    category_names = fields.List(fields.String, dump_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)
    cover = fields.URL()

    def get_creator(self, obj):
        try:
            creator_id = obj.creator_id
            user = get_user(creator_id)
            return user.username
        except Exception:
            traceback.print_exc()
        


class ItemSchema(Schema):
    id = fields.String(dump_only=True)
    question = fields.String(required=True)
    answer = fields.String(required=True)
    refer = fields.String(default='')
    point_id = fields.String(required=True)
    point_name = fields.Method('get_point_name',dump_only=True)
    related_point_ids = fields.List(fields.String, default=[])
    related_point_names = fields.Method('get_related_point_names', default=[],dump_only=True)
    subject_id = fields.String(required=True)
    subject_name = fields.Method('get_subject_name',dump_only=True)
    item_type = fields.String(required=True,choices=('theory', 'application', 'general_knowledge'))
    sequence = fields.Int(required=True)
    creator_id = fields.String(required=True)
    creator_name = fields.Method('get_creator_name',dump_only=True)

    def get_creator_name(self,obj):
        try:
            creator_id = obj.creator_id
            user = get_user(creator_id)
            return user.username
        except Exception:
            traceback.print_exc()

    def get_point_name(self,obj):
        try:
            point = Point.objects.get(id=obj.point_id)
            return point.name
        except Exception:
            traceback.print_exc()

    def get_subject_name(self,obj):
        try:
            subject = Subject.objects.get(id=obj.subject_id)
            return subject.name
        except Exception:
            traceback.print_exc()
    
    def get_related_point_names(self,obj):
        try:
            related_point_names = []
            related_point_ids = obj.related_point_ids
            if related_point_ids:
                for related_point_id in related_point_ids:
                    related_point = Point.objects.get(id=related_point_id)
                    related_point_name = related_point.name
                    related_point_names.append(related_point_name)
            return related_point_names
        except Exception:
            traceback.print_exc()
    
        


class PointSchema(Schema):
    id = fields.String(dump_only=True)
    subject_id = fields.String(required=True)
    subject_name = fields.String(dump_only=True)
    name = fields.String(required=True)
    # level = fields.Int(required=True)


class PointRelationSchema(Schema):
    id = fields.String(dump_only=True)
    subject_id = fields.String(required=True)  # 关联课程
    subject_name = fields.String(dump_only=True)
    from_node_type = fields.String(required=True, choices=('subject', 'point'))  # from节点类型定义，节点1只能是point
    from_node_type_display = fields.String(required=True,dump_only=True )  
    from_node_id = fields.String(required=True)  # from节点id
    from_node_name = fields.String(dump_only=True)
    relation = fields.String(required=True, choices=['contains', ])  # 节点间关系
    relation_display = fields.String(required=True,dump_only=True )
    to_node_type = fields.String(required=True, choices=('point',))  # to节点类型,如果节点1的类型为subject，那么节点2的类型只能是point
    to_node_type_display = fields.String(required=True,dump_only=True )  
    to_node_id = fields.String(required=True)  # to节点id
    to_node_name = fields.String(dump_only=True)
    sequence = fields.Int(min_value=1, default=1)  # 标识序号


class StudyItemSchema(Schema):
    id = fields.String(required=True)
    question = fields.String(dump_only=True)
    answer = fields.String(dump_only=True)
    refer = fields.String(dump_only=True)
    # point = fields.List(fields.String, load_only=True)
    point_name = fields.Method('get_point_name',dump_only=True)
    subject_id = fields.String(load_only=True)
    subject_name = fields.String(dump_only=True)


    def get_point_name(self,obj):
        try:
            point = Point.objects.get(id=obj.point_id)
            return point.name
        except Exception:
            traceback.print_exc()
