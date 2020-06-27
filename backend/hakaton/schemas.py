from marshmallow import Schema, fields, post_load
from .models import Type, Element


class ElementSchema(Schema):
    name = fields.String()
    type = fields.String()

    @post_load
    def make_obj(self, data, **kwargs):
        return Element(**data)


class TypeSchema(Schema):
    name = fields.String()
    elements = fields.List(fields.Nested(ElementSchema), default=[])
    editable = fields.Boolean(default=True)
    version = fields.Integer()
    updated = fields.DateTime(dump_only=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return Type(**data)
