import uuid
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import ProductModel, VersionModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("versions", __name__, description="business central product version")


@blp.route("/version/<string:version_id>")
class Version(MethodView):
    def get(self, version_id):
        version = VersionModel.query.get_or_404(version_id)
        return "Ok", 200

    def patch(self, version_id):
        request_data = request.get_json()
        version = VersionModel.query.get_or_404(version_id)
        version.tag = request_data["tag"]
        version.price = request_data["price"]
        db.session.add(version)
        db.session.commit()
        return "ok", 200

    def delete(self, version_id):
        version = ProductModel.query.get_or_404(version_id)
        db.session.delete(version)
        db.session.commit()
        return "Ok", 201


@blp.route("/version")
class VersionList(MethodView):

    def get(self):
        print(VersionModel.query.all())
        return "ok", 200


@blp.route("/product/<string:product_id>/version")
class ProductVersionList(MethodView):

    def get(self, product_id):
        response_data = {
            "versions": []
        }
        print(VersionModel.query.filter_by(product_id=product_id).all())
        return "ok", 200

    def post(self, product_id):
        request_data = request.get_json()
        ProductModel.query.get_or_404(product_id)
        version = VersionModel(**request_data)
        version.product_id = product_id
        try:
            db.session.add(version)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Version is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the version")

        return str(version.id), 200
