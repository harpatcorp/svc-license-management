import secrets

import models
import os

from sqldb import db
from datetime import timedelta
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.product import blp as ProductBlueprint
from resources.version import blp as VersionBlueprint
from resources.version import blp2 as VersionAppBlueprint
from resources.transaction import blp as TransactionBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "License REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity["is_admin"]:
            return {"is_admin": True}
        return {"is_admin": False}

    with app.app_context():
        db.create_all()

    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(VersionBlueprint)
    api.register_blueprint(VersionAppBlueprint)
    api.register_blueprint(TransactionBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
