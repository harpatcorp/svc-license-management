import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import ProductModel, VersionModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schema import VersionSchema

blp = Blueprint("Version", __name__, description="business central product version")


@blp.route("/version/<string:version_id>")
class Version(MethodView):

    @blp.response(200, VersionSchema)
    def get(self, version_id):
        version = VersionModel.query.get_or_404(version_id)
        return version

    @blp.arguments(VersionSchema)
    @blp.response(200, VersionSchema)
    def patch(self, version_data, version_id):
        version = VersionModel.query.get_or_404(version_id)
        version.modified_on = datetime.datetime.now()
        db.session.add(**version_data)
        db.session.commit()
        return version

    @blp.response(204)
    def delete(self, version_id):
        version = VersionModel.query.get_or_404(version_id)
        db.session.delete(version)
        db.session.commit()
        return 204


@blp.route("/version")
class VersionList(MethodView):

    @blp.response(200, VersionSchema(many=True))
    def get(self):
        versions = VersionModel.query.all()
        return versions


@blp.route("/product/<string:product_id>/version")
class ProductVersionList(MethodView):

    @blp.response(200, VersionSchema(many=True))
    def get(self, product_id):
        versions = VersionModel.query.filter_by(product_id=product_id).all()
        return versions

    @blp.arguments(VersionSchema)
    @blp.response(201, VersionSchema)
    def post(self, version_data, product_id):
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
