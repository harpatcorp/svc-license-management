import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from sqldb import db
from schema import TransactionSchema
from models import TransactionModel, UserModel, VersionModel, ProductModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Transaction", __name__, description="business central products sell transactions")


@blp.route("/transaction/<string:transaction_id>")
class Transaction(MethodView):

    @jwt_required()
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        '''
            This end point is used to retrive transaction based on transaction id
            Note: Admin access is required
        '''

        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        transaction = TransactionModel.query.get_or_404(transaction_id)
        return transaction


@blp.route("/user/<string:user_id>/transaction")
class UserTransactionList(MethodView):

    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        '''
            This end point is used to retrive transaction based on user id
        '''

        transactions = TransactionModel.query.filter_by(user_id=user_id, paid=True).all()
        return transactions


@blp.route("/transaction")
class TransactionList(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        '''
            This end point is used to retrive transactions
            Note: Admin access is required
        '''

        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        transactions = TransactionModel.query.all()
        return transactions

    @jwt_required()
    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction_data):
        '''
            This end point is used to add a transaction
        '''

        UserModel.query.get_or_404(transaction_data["user_id"])
        ProductModel.query.get_or_404(transaction_data["product_id"])
        VersionModel.query.get_or_404(transaction_data["version_id"])

        transaction = TransactionModel(**transaction_data)
        transaction.ordered_on = datetime.datetime.now()
        transaction.expired_on = datetime.datetime.now() + (datetime.timedelta(days=365)*5)

        try:
            db.session.add(transaction)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Transaction is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the transaction")

        return transaction
