from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, BooleanField


class Carousel(Document):
    title = StringField(required=True,verbose_name="标题")
    image_url = StringField(required=True,verbose_name="图片链接")
    link_url = StringField(verbose_name="跳转链接")
    is_active = BooleanField(default=True,verbose_name="是否可用")
    creator_id = StringField(required=True,verbose_name="创建都id")
    created_at = DateTimeField(default=datetime.utcnow,verbose_name="创建时间")


    def __repr__(self):
        return "<Carousel %s>" % self.title

    def __str__(self):
        return "{}".format(self.title)