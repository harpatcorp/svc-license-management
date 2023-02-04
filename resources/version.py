import uuid
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import products, versions

blp = Blueprint("versions", __name__, description="business central product version")


@blp.route("/version/<string:version_id>")
class Version(MethodView):
    def get(self, version_id):
        for version in versions:
            if version["id"] == version_id:
                return version, 200
        else:
            abort(404, message=f"Version with version id {version_id} is not found")

    def patch(self, version_id):
        request_data = request.get_json()
        for version in versions:
            if version["id"] == id:
                version["tag"] = request_data["tag"]
                version["price"] = request_data["price"]
                return version, 204
        else:
            abort(404, message=f"Version with version id {version_id} is not found")

    def delete(self, version_id):
        for version in versions:
            if version["id"] == id:
                versions.remove(version)
                return version, 204
        else:
            abort(404, message=f"Version with version id {version_id} is not found")


@blp.route("/version")
class VersionList(MethodView):

    def get(self):
        response_data = {
            "versions": versions
        }
        return response_data, 200


@blp.route("/product/<string:product_id>/version")
class ProductVersionList(MethodView):

    def get(self, product_id):
        response_data = {
            "versions": []
        }
        for product in products:
            if product["id"] == product_id:
                for version in versions:
                    if version["product_id"] == product_id:
                        response_data["versions"].append(version)

                if len(response_data["versions"]) == 0:
                    abort(404, message=f"Version with product id {product_id} is not found")
                else:
                    return response_data, 200
            else:
                abort(400, message=f"Version with product id {product_id} is not found")

    def post(self, product_id):
        request_data = request.get_json()
        for product in products:
            if product["id"] == id:
                if len(request_data["tag"]) == 0 or request_data["price"] <= 0.0:
                    abort(400, message="Please add tag or price in the body")
                else:
                    version = {
                        "id": str(uuid.uuid4()),
                        "product_id": id,
                        "tag": request_data["tag"],
                        "currency": "USD",
                        "price": request_data["price"],
                        "path": "",
                        "created_on": str(datetime.date.today()),
                        "modified_on": str(datetime.date.today())
                    }
                    versions.append(version)
                    return version, 201
            else:
                abort(404, message=f"Version with product id {product_id} is not found")
