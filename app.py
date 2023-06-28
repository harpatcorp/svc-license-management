import secrets

from sqldb import db
from datetime import timedelta
from config import DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.product import blp as ProductBlueprint
from resources.version import blp as VersionBlueprint
from resources.version import blp2 as VersionAppBlueprint
from resources.transaction import blp as TransactionBlueprint
from resources.user import blp as UserBlueprint
from resources.payment import blp as PaymentBlueprint
from resources.license import blp as LicenseBlueprint


def create_app(db_url=None):
    '''
        This function is used to configure flask application.
    '''
    
    app = Flask(__name__)

    app.config["API_TITLE"] = "License REST API"
    app.config["API_VERSION"] = "v1"

    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "postgresql://" + DB_USER + ":" + DB_PASS + "@" + DB_IP + ":" +DB_PORT + "/" +DB_NAME
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity["is_admin"]:
            return {"is_admin": True}
        return {"is_admin": False}

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)

    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(VersionBlueprint)
    api.register_blueprint(VersionAppBlueprint)
    api.register_blueprint(TransactionBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PaymentBlueprint)
    api.register_blueprint(LicenseBlueprint)

    return app


if __name__ == "__main__":

    flask_app = create_app()
    flask_app.run(host="0.0.0.0",debug=True, port=8080)