import uuid
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import versions, transactions, users

blp = Blueprint("transactions", __name__, description="business central products sell transactions")


@blp.route("/transaction/<string:transaction_id>")
class Transaction(MethodView):
    def get(self, transaction_id):
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return transaction, 200
        else:
            abort(404, message=f"Transaction with transaction id {transaction_id} is not found")


@blp.route("user/<string:user_id>/transaction")
class UserTransactionList(MethodView):
    def get(self, user_id):
        response_data = {
            "transactions": []
        }
        for user in users:
            if user["id"] == user_id:
                for transaction in versions:
                    if transaction["user_id"] == user_id:
                        response_data["transactions"].append(transaction)

                return response_data, 200
            else:
                abort(404, message=f"User with user id {user_id} is not found")


@blp.route("/transaction")
class TransactionList(MethodView):
    def get(self):
        response_data = {
            "transactions": transactions
        }
        return response_data, 200

    def post(self):
        request_data = request.get_json()

        transaction = {
            "id": str(uuid.uuid4()),
            "user_id": request_data["user_id"],
            "product_id": request_data["product_id"],
            "version_id": request_data["version_id"],
            "qty": request_data["qty"],
            "currency": "USD",
            "price": 25,
            "total_amt": 25,
            "ordered_on": str(datetime.date.today()),
            "expired_on": str(datetime.date.today() + datetime.timedelta(days=5 * 365))
        }

        transactions.append(transaction)

        return transaction, 201
