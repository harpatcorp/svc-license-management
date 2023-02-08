from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=False)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)


class VersionSchema(Schema):
    id = fields.Str(dump_only=True)
    product_id = fields.Str(dump_only=True)
    tag = fields.Str(required=True)
    currency = fields.Str(dump_only=True)
    price = fields.Float(required=True)
    path = fields.Str(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)
