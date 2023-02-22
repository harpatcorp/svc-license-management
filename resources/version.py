import datetime
import os
import uuid

from flask import request
from flask import send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import ProductModel, VersionModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schema import VersionSchema
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.utils import secure_filename

blp = Blueprint("Version", __name__, description="business central product version")
blp2 = Blueprint("Version App", __name__, description="business central product version app")
APP_PATH = os.path.join("/home/harshil/PycharmProjects/api_server/data/app")


@blp.route("/version/<string:version_id>")
class Version(MethodView):

    @jwt_required()
    @blp.response(200, VersionSchema)
    def get(self, version_id):
        version = VersionModel.query.get_or_404(version_id)
        return version

    @jwt_required()
    @blp.arguments(VersionSchema)
    @blp.response(200, VersionSchema)
    def patch(self, version_data, version_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        version = VersionModel.query.get_or_404(version_id)
        version.tag = version_data["tag"]
        version.price = version_data["price"]
        version.modified_on = datetime.datetime.now()

        db.session.add(version)
        db.session.commit()

        return version

    @jwt_required()
    @blp.response(204)
    def delete(self, version_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        version = VersionModel.query.get_or_404(version_id)

        db.session.delete(version)
        db.session.commit()

        return 204


@blp.route("/version")
class VersionList(MethodView):
    @jwt_required()
    @blp.response(200, VersionSchema(many=True))
    def get(self):
        versions = VersionModel.query.all()
        return versions


@blp.route("/product/<string:product_id>/version")
class ProductVersionList(MethodView):
    @jwt_required()
    @blp.response(200, VersionSchema(many=True))
    def get(self, product_id):
        versions = VersionModel.query.filter_by(product_id=product_id).all()
        return versions

    @jwt_required()
    @blp.arguments(VersionSchema)
    @blp.response(201, VersionSchema)
    def post(self, version_data, product_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        ProductModel.query.get_or_404(product_id)

        version = VersionModel(**version_data)
        version.product_id = product_id

        version.created_on = datetime.datetime.now()
        version.modified_on = datetime.datetime.now()

        try:
            db.session.add(version)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Version is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the version")

        return version


@blp2.route("/version-app/<string:version_id>")
class VersionApp(MethodView):

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {"app"}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @jwt_required()
    @blp.response(201)
    def post(self, version_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        if 'app_file' not in request.files:
            return abort(400, message="app_file is not provided")

        version = VersionModel.query.get_or_404(version_id)

        app_file = request.files['app_file']

        if app_file.filename == '':
            return abort(400, message="file name is not provided")
        if app_file and VersionApp.allowed_file(app_file.filename):
            if version.path is not None:
                if os.path.exists(version.path):
                    os.remove(version.path)

            filename = str(uuid.uuid4())+".app"
            filepath = str(os.path.join(APP_PATH, filename))

            app_file.save(filepath)

            version.path = filepath

            db.session.add(version)
            db.session.commit()

            return 201

    @jwt_required()
    @blp.response(200)
    def get(self, version_id):
        version = VersionModel.query.get_or_404(version_id)

        if version.path is None:
            abort(404, message="Sorry! app file is not available for product")

        return send_file(version.path, download_name=str(version.product_id)+"-"+str(version.id)+".app")
