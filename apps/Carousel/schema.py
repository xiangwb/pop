from datetime import datetime
from marshmallow import Schema, fields


class CarouselSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    image_url = fields.String(required=True)
    link_url = fields.String()
    is_active = fields.Boolean(default=True)
    created_at = fields.DateTime(default=datetime.utcnow)