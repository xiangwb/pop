import traceback

from marshmallow import Schema, fields
from apps.course.adapter import get_user
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

    def get_creator(self, obj):
        try:
            creator_id = obj.creator_id
            user = get_user(creator_id)
            return user.get('username')
        except Exception:
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())


class ItemSchema(Schema):
    id = fields.String(dump_only=True)
    question = fields.String(required=True)
    answer = fields.String(required=True)
    refer = fields.String(required=False, default='')
    point_id = fields.String(required=True)
    point_name = fields.String(dump_only=True)
    related_point_ids = fields.List(fields.String, default=[])
    related_point_names = fields.List(fields.String, default=[])
    subject_id = fields.String(load_only=True)
    subject_name = fields.String(dump_only=True)
    item_type = fields.String(required=True)
    sequence = fields.Int(required=True)
    creator_name = fields.String(required=True)


class PointSchema(Schema):
    id = fields.String(dump_only=True)
    subject_id = fields.String(load_only=True, required=True)
    subject_name = fields.String(dump_only=True)
    name = fields.String(required=True)
    # level = fields.Int(required=True)


class PointRelationSchema(Schema):
    id = fields.String(dump_only=True)
    subject_id = fields.String(load_only=True, required=True)  # 关联课程
    subject_name = fields.String(dump_only=True)
    from_node_type = fields.String(required=True, choices=('subject', 'point'))  # from节点类型定义，节点1只能是point
    from_node_id = fields.String(required=True)  # from节点id
    from_node_name = fields.String(dump_only=True)
    relation = fields.String(required=True, choices=['contains', ])  # 节点间关系
    to_node_type = fields.String(required=True, choices=('point',))  # to节点类型,如果节点1的类型为subject，那么节点2的类型只能是point
    to_node_id = fields.String(required=True)  # to节点id
    to_node_name = fields.String(dump_only=True)
    sequence = fields.Int(min_value=1, default=1)  # 标识序号


class StudyItemSchema(Schema):
    id = fields.String(required=True)
    question = fields.String(dump_only=True)
    answer = fields.String(load_only=True, required=False)
    refer = fields.String(dump_only=True)
    # point = fields.List(fields.String, load_only=True)
    point_name = fields.String(dump_only=True)
    subject_id = fields.String(load_only=True)
    subject_name = fields.String(dump_only=True)
