from mongoengine import signals

from extensions import db
import mongoengine as mg


class SubjectCategory(db.Document):
    """
    课程分类模型：树形结构
    """
    name = mg.StringField(required=True, max_length=100)
    parent_id = mg.StringField(required=False)
    path = mg.StringField(required=False)

    def __repr__(self):
        return "<Category %s>" % self.name

    def __str__(self):
        return "{}_{}".format(self.path, self.name)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.parent_id is None:
            document.path = '/'
        else:
            # document.path = '{}/{}'.format(document.parent.path, document.parent.name)
            parent_id = document.parent_id
            parent_subject_category = SubjectCategory.objects.get(id=parent_id)
            if parent_subject_category.path == '/':
                document.path = parent_subject_category.path + parent_subject_category.name
            else:
                document.path = parent_subject_category.path + '/' + parent_subject_category.name

    meta = {
        'indexes': [{'fields': ['name', 'path'], 'unique': True}, ]
    }


signals.pre_save.connect(SubjectCategory.pre_save, sender=SubjectCategory)


class Subject(db.Document):
    """
    课程模型
    """
    name = mg.StringField(required=True, max_length=100, unique=True)
    creator_id = mg.StringField(required=True)
    category_ids = mg.ListField(mg.StringField())
    cover = mg.StringField(required=False)
    desc = mg.StringField(required=True)

    def __repr__(self):
        return "<Subject %s>" % self.name

    def __str__(self):
        return "{}".format(self.name)


class Point(db.Document):
    """
    课程知识点
    """
    subject_id = mg.StringField(required=True)
    # level = mg.IntField(required=True)
    name = mg.StringField(required=True, max_length=100, unique=True)

    def __repr__(self):
        return "<Point %s_%s>" % (self.subject_id, self.name)

    def __str__(self):
        return "{}".format(self.name)

    meta = {
        'indexes': [{'fields': ['subject_id', 'name'], 'unique': True}, ]
    }


class Item(db.Document):
    """
    问题条目
    """

    question = mg.StringField(required=True)
    answer = mg.StringField(required=False)
    refer = mg.StringField()
    point_id = mg.StringField(required=True)
    # point_name = mg.StringField(required=True)
    related_point_ids = mg.ListField(mg.StringField())
    # related_point_names = mg.ListField(mg.StringField())
    subject_id = mg.StringField(required=True)
    # subject_name = mg.StringField(required=True)
    item_type = mg.StringField(required=True, choices=['theory', 'application', 'general_knowledge'])
    creator_id = mg.StringField(required=True)
    # creator_name = mg.StringField(required=True)
    sequence = mg.IntField(min_value=1, default=1)

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def __repr__(self):
        return "<Item %s>" % self.id


class PointRelation(db.Document):
    """
    知识点图谱三元组
    """
    subject_id = mg.StringField(required=True)  # 关联课程
    from_node_type = mg.StringField(required=True, choices=('subject', 'point'))  # from节点类型定义，节点1只能是point
    from_node_id = mg.StringField(required=True)  # from节点id
    relation = mg.StringField(required=True, choices=['contains', ])  # 节点间关系
    to_node_type = mg.StringField(required=True, choices=('point',))  # to节点类型,如果节点1的类型为subject，那么节点2的类型只能是point
    to_node_id = mg.StringField(required=True)  # to节点id
    sequence = mg.IntField(min_value=1, default=1)  # 标识序号

    # graph = mg.DictField(required=True)

    def __repr__(self):
        return "<PointRelation {}>".format(self.relation)


class UserSubject(db.Document):
    """
    用户课程情况
    detail数据结构：
    {
        "points":{
        },
        "items":{
        },
        "latest":{"item_id":"a1d323brd","answer":1}
    }
    """
    user_id = mg.StringField(required=True)  # 用户ID
    subject_id = mg.StringField(required=True)
    detail = mg.DictField(required=True)  # 知识点掌握情况

    def __repr__(self):
        return "<UserItem {}".format(self.user_id)
