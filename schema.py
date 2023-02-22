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
    currency = fields.Str(dump_only=True, default="INR")
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
    order_id = fields.Str(dump_only=True)
    paid = fields.Boolean(dump_only=True)
    active = fields.Boolean(dump_only=True)
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


class ProductVersionSchema(ProductSchema):
    versions = fields.List(fields.Nested(VersionSchema()), dump_only=True)


class PaymentIntegrationInputSchema(Schema):
    user_id = fields.Str(required=True, load_only=True)
    product_id = fields.Str(required=True, load_only=True)
    version_id = fields.Str(required=True, load_only=True)
    customer_id = fields.Str(required=True, load_only=True)
    customer_name = fields.Str(required=True, load_only=True)
    customer_email = fields.Str(required=True, load_only=True)
    customer_phone = fields.Str(required=True, load_only=True)
    payment_methods = fields.Str(required=True, load_only=True)
    order_amount = fields.Float(required=True, load_only=True)
    order_currency = fields.Str(required=True, load_only=True, default="INR")
    return_url = fields.Str(required=True, load_only=True)


class GenericMessageSchema(Schema):
    message = fields.Str(required=True, dump_only=True)
