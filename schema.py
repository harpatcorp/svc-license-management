from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)


class ProductInsertSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.List(fields.Str(), required=False)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)


class VersionSchema(Schema):
    id = fields.Str(dump_only=True)
    product_id = fields.Str(dump_only=True)
    tag = fields.Str(required=True)
    currency = fields.Str(dump_only=True, default="USD")
    price = fields.Float(required=True)
    path = fields.Str(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)


class TransactionSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    product_id = fields.Str(required=True)
    version_id = fields.Str(required=True)
    qty = fields.Float(required=True)
    currency = fields.Str(dump_only=True)
    price = fields.Float(required=True)
    total_amt = fields.Float(required=True)
    ordered_on = fields.DateTime(dump_only=True)
    expired_on = fields.DateTime(dump_only=True)


class UserRegistrationSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password_1 = fields.Str(required=True)
    password_2 = fields.Str(required=True)
    is_admin = fields.Boolean(required=True)
    created_on = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AccessTokenSchema(Schema):
    access_token = fields.Str(dump_only=True)
    expired_in = fields.Int(dump_only=True)
