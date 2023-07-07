import datetime
import os
import uuid

from flask import request
from flask import send_file
from flask.views import MethodView
from flask import current_app as app
from flask_smorest import Blueprint, abort

from sqldb import db
from schema import VersionSchema
from models import ProductModel, VersionModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import get_jwt, jwt_required
from config import APP_PATH

blp = Blueprint("Version", __name__, description="business central product version")
blp2 = Blueprint("Version App", __name__, description="business central product version app")


@blp.route("/version/<string:version_id>")
class Version(MethodView):

    @blp.response(200, VersionSchema)
    def get(self, version_id):
        '''
            This end point is used to retrieve version of the product based on product id
        '''
        app.logger.info("Version Id: {}".format(version_id))
        version = VersionModel.query.get_or_404(version_id)
        return version

    @jwt_required()
    @blp.arguments(VersionSchema)
    @blp.response(200, VersionSchema)
    def patch(self, version_data, version_id):
        '''
            This end point is used to update version of the product based on the product id and version id
            Note: Admin access is required
        '''
        app.logger.info("Version Id: {}".format(version_id))
        app.logger.info("Version Data: {}".format(version_data))
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        version = VersionModel.query.get_or_404(version_id)
        version.tag = version_data["tag"]
        version.price = version_data["price"]
        version.modified_on = datetime.datetime.now()

        db.session.add(version)
        db.session.commit()

        app.logger.info("Version Id {} is updated".format(version_id))
        return version

    @jwt_required()
    @blp.response(204)
    def delete(self, version_id):
        '''
            This end point is used to delete version of the product based on version id
            Note: Admin access is required
        '''
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        version = VersionModel.query.get_or_404(version_id)

        db.session.delete(version)
        db.session.commit()

        app.logger.info("Version Id {} is deleted".format(version_id))
        return 204


@blp.route("/version")
class VersionList(MethodView):
    
    @jwt_required()
    @blp.response(200, VersionSchema(many=True))
    def get(self):
        ''''
            This end point is used to retrive all versions of availabe products
            Note: Admin access is required
        '''
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        versions = VersionModel.query.all()
        return versions


@blp.route("/product/<string:product_id>/version")
class ProductVersionList(MethodView):
    
    @jwt_required()
    @blp.response(200, VersionSchema(many=True))
    def get(self, product_id):
        '''
            This end point is used to retrive version of a product based on the product id
        '''
        app.logger.info("Product Id: {}".format(product_id))
        versions = VersionModel.query.filter_by(product_id=product_id).all()
        return versions

    @jwt_required()
    @blp.arguments(VersionSchema)
    @blp.response(201, VersionSchema)
    def post(self, version_data, product_id):
        '''
            This end point is used to upload version of a product based on the product id
            Note: Admin access is required
        '''
        
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
