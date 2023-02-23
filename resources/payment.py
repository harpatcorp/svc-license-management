import datetime
import uuid

import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import TransactionModel, UserModel, VersionModel, ProductModel
from schema import PaymentIntegrationInputSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

blp = Blueprint("Payment", __name__, description="payment for business central")


@blp.route("/payment")
class UserPayment(MethodView):

    PAYMENT_URL = "https://sandbox.cashfree.com/pg/orders"
    CLIENT_ID = "321006c79ba794b84a59522df8600123"
    CLIENT_SECRET = "1ea7cb51ebbb80442562b5bedf891f0841f6d8d1"

    @jwt_required()
    @blp.arguments(PaymentIntegrationInputSchema)
    def post(self, payment_data):
        UserModel.query.get_or_404(payment_data["user_id"])
        ProductModel.query.get_or_404(payment_data["product_id"])
        VersionModel.query.get_or_404(payment_data["version_id"])

        payload = {
            "customer_details": {
                "customer_id": payment_data["customer_id"],
                "customer_name": payment_data["customer_name"],
                "customer_email": payment_data["customer_email"],
                "customer_phone": payment_data["customer_phone"]
            },
            "order_meta": {
                "return_url": payment_data["return_url"]
            },
            "order_meta": {"payment_methods": payment_data["payment_methods"]},
            "order_id": str(uuid.uuid4()),
            "order_amount": payment_data["order_amount"],
            "order_currency": payment_data["order_currency"]
        }
        headers = {
            "accept": "application/json",
            "x-client-id": UserPayment.CLIENT_ID,
            "x-client-secret": UserPayment.CLIENT_SECRET,
            "x-api-version": "2022-09-01",
            "content-type": "application/json"
        }

        response = requests.post(UserPayment.PAYMENT_URL, json=payload, headers=headers)

        if response.status_code == 200:
            transaction_data = {
                "user_id": payment_data["user_id"],
                "product_id": payment_data["product_id"],
                "version_id": payment_data["version_id"],
                "qty": 1,
                "price": payment_data["order_amount"],
                "order_id": payload["order_id"],
                "paid": False,
                "total_amt": payment_data["order_amount"]
            }

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

            return response.json(), response.status_code


@blp.route("/payment/order/<string:order_id>")
class UserPaymentOrder(MethodView):

    ORD_URL = "https://sandbox.cashfree.com/pg/orders/"
    CLIENT_ID = "321006c79ba794b84a59522df8600123"
    CLIENT_SECRET = "1ea7cb51ebbb80442562b5bedf891f0841f6d8d1"

    @blp.response(200)
    def get(self, order_id):
        url = UserPaymentOrder.ORD_URL+order_id

        headers = {
            "accept": "application/json",
            "x-client-id": UserPaymentOrder.CLIENT_ID,
            "x-client-secret": UserPaymentOrder.CLIENT_SECRET,
            "x-api-version": "2021-05-21"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if response.json()["order_status"] == "PAID":
                transactions = TransactionModel.query.filter_by(order_id=order_id, paid=False).all()
                for transaction in transactions:
                    transaction.paid = True
                    transaction.expired_on = datetime.datetime.now() + (datetime.timedelta(days=365)*5)
                    db.session.add(transaction)
                    db.session.commit()
                return response.json(), response.status_code
            else:
                return response.json(), 400
        else:
            return response.json(), response.status_code
