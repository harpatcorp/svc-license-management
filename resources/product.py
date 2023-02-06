import uuid
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import products
from sqldb import db
from models import ProductModel
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Products", __name__, description="Business central extensions as a product")


@blp.route("/product/<string:product_id>")
class Product(MethodView):

    def get(self, product_id):
        for product in products:
            if product["id"] == product_id:
                return product, 200
        else:
            abort(404, message=f"Product with product id {product_id} is not found")

    def patch(self, product_id):
        request_data = request.get_json()
        for product in products:
            if product["id"] == product_id:
                product["name"] = request_data["name"]
                product["description"] = request_data["description"]
                return product, 204
        else:
            abort(404, message=f"Product with product id {product_id} is not found")

    def delete(self, product_id):
        for product in products:
            if product["id"] == product_id:
                products.remove(product)
                return product, 204
        else:
            abort(404, message=f"Product with product id {product_id} is not found")


@blp.route("/product")
class ProductList(MethodView):

    def post(self):
        request_data = request.get_json()
        product = ProductModel(**request_data)
        print(f"id:{product.id}")
        print(f"name:{product.name}")
        print(f"desc:{product.description}")
        # print(f"version:{product.versions}")
        print(f"image:{product.image}")
        print(f"created_on:{product.image}")
        # try:
        db.session.add(product)
        print("test")
        db.session.commit()
        print(f"id:{product.id}")
        print(f"name:{product.name}")
        print(f"desc:{product.description}")
        # except SQLAlchemyError:
        #     abort(500, message="An error occurred while inserting the product.")

        return "ok",200

    def get(self):
        response_data = {
            "products": products
        }
        return ProductModel.query.all(), 200
