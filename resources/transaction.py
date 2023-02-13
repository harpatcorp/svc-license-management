import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import TransactionModel
from schema import TransactionSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Transaction", __name__, description="business central products sell transactions")


@blp.route("/transaction/<string:transaction_id>")
class Transaction(MethodView):

    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        transaction = TransactionModel.query.get_or_404(transaction_id)
        return transaction


@blp.route("/user/<string:user_id>/transaction")
class UserTransactionList(MethodView):
    @blp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        transactions = TransactionModel.query.filter_by(user_id=user_id).all()
        return transactions


@blp.route("/transaction")
class TransactionList(MethodView):
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        transactions = TransactionModel.query.all()
        return transactions

    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction_data):
        transaction = TransactionModel(**transaction_data)
        transaction.ordered_on = datetime.datetime.now()
        transaction.expired_on = datetime.datetime.now()

        try:
            db.session.add(transaction)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Transaction is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the transaction")

        return transaction
