import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import UserModel
from schema import UserRegistrationSchema, UserLoginSchema, AccessTokenSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from passlib.hash import pbkdf2_sha256

blp = Blueprint("User", __name__, description="user of license management system")


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserRegistrationSchema)
    def get(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    @blp.response(204)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return 204


@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserRegistrationSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        users = UserModel.query.all()
        return users

    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserRegistrationSchema)
    def post(self, user_data):
        if user_data["password_1"] != user_data["password_2"]:
            abort(422, message="password_1 and password_2 does not match")

        user = UserModel(
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password_1=pbkdf2_sha256.hash(user_data["password_1"]),
            password_2=pbkdf2_sha256.hash(user_data["password_2"]),
            is_admin=user_data["is_admin"]
        )
        user.created_on = datetime.datetime.now()

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the transaction")

        return user


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserLoginSchema)
    @blp.response(200, AccessTokenSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password_1):
            access_token = create_access_token(identity=
                                               {
                                                   "user_id": user.id,
                                                   "is_admin": user.is_admin
                                               }
            )
            return {"access_token": access_token, "expired_in": 3600}

        abort(401, message="Invalid credentials.")
