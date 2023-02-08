import datetime
from email import message

import utils
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import ProductModel
from schema import ProductSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Products", __name__, description="Business central extensions as a product")


@blp.route("/product/<string:product_id>")
class Product(MethodView):

    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def patch(self, product_data, product_id):
        product = ProductModel.query.get_or_404(product_id)
        product.name = product_data["name"]
        product.description = product_data["description"]
        try:
            product.image = product_data["image"]
        except KeyError:
            print("Image key not found")
        product.modified_on = datetime.datetime.now()
        db.session.add(product)
        db.session.commit()
        return product

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return 204


@blp.route("/product")
class ProductList(MethodView):

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        product = ProductModel(**product_data)
        if not utils.isBase64(str(product.image)):
            abort(400, message="Image is not converted in base64.")
        product.created_on = datetime.datetime.now()
        product.modified_on = datetime.datetime.now()
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Product is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the product")

        return product

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        products = ProductModel.query.all()
        return products
