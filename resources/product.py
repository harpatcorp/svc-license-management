import uuid
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import products

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
        if len(request_data["name"]) == 0 or len(request_data["description"]) == 0:
            abort(400, message="Please add name or description in the body")
        else:
            product = {
                "id": str(uuid.uuid4()),
                "name": request_data["name"],
                "description": request_data["description"],
                "version_id": {},
                "image": "",
                "created_on": str(datetime.date.today()),
                "modified_on": str(datetime.date.today())
            }
            products.append(product)
            return product, 201

    def get(self):
        response_data = {
            "products": products
        }
        return response_data, 200
