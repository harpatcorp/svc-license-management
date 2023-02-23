import io
import uuid
import json
import datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqldb import db
from models import TransactionModel, UserModel, VersionModel, ProductModel
from flask_jwt_extended import jwt_required
from flask import send_file
from toolkit import EncDec
from schema import GenericMessageSchema

blp = Blueprint("License", __name__, description="license for business central")


@blp.route("/transaction/<string:transaction_id>/license/")
class GenerateLicense(MethodView):

    ORIGINAL_FILE_PATH = "/home/harshil/PycharmProjects/api_server/data/license/original_data/"
    ENCRYPTED_FILE_PATH = "/home/harshil/PycharmProjects/api_server/data/license/encrypted_data/"

    @jwt_required()
    @blp.response(200)
    def post(self, transaction_id):
        transaction = TransactionModel.query.get_or_404(transaction_id)

        if transaction.paid is False:
            abort(400, message="Transaction payment is not completed")
        else:
            response_body = dict()

            file_name = str(uuid.uuid4()) + ".lic"

            response_body["id"] = transaction.id
            response_body["user_id"] = transaction.user_id
            response_body["product_id"] = transaction.product_id
            response_body["version_id"] = transaction.version_id
            response_body["qty"] = transaction.qty
            response_body["currency"] = transaction.currency
            response_body["price"] = transaction.price
            response_body["currency"] = transaction.currency
            response_body["total_amt"] = transaction.total_amt
            response_body["order_id"] = transaction.order_id
            response_body["paid"] = transaction.paid
            response_body["ordered_on"] = str(transaction.ordered_on)
            response_body["expired_on"] = str(transaction.expired_on)

            with open(GenerateLicense.ORIGINAL_FILE_PATH + file_name, "w") as data:
                data.write(json.dumps(response_body))

            EncDec().encrypt_file(GenerateLicense.ORIGINAL_FILE_PATH + file_name,
                                  GenerateLicense.ENCRYPTED_FILE_PATH + file_name)

        return send_file(path_or_file=GenerateLicense.ENCRYPTED_FILE_PATH + file_name, download_name="license.lic")


@blp.route("/license/activate")
class ActivateLicense(MethodView):

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {"lic"}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @jwt_required()
    @blp.response(200, GenericMessageSchema)
    def post(self):
        if 'lic_file' not in request.files:
            return abort(400, message="lic_file is not provided")

        lic_file = request.files['lic_file']

        if lic_file.filename == '':
            return abort(400, message="file name is not provided")
        if lic_file and ActivateLicense.allowed_file(lic_file.filename):
            request_file = io.BytesIO(EncDec().decrypt_file_data(lic_file.stream.read()))
            request_data = json.load(request_file)

            transaction = TransactionModel.query.get_or_404(request_data["id"])

            UserModel.query.get_or_404(request_data["user_id"])
            ProductModel.query.get_or_404(request_data["product_id"])
            VersionModel.query.get_or_404(request_data["version_id"])

            if datetime.datetime.strptime(request_data["expired_on"],
                                          "%Y-%m-%d %H:%M:%S.%f") <= datetime.datetime.now():
                abort(400, message="license is expired on {}".format(request_data["expired_on"]))

            if transaction.active:
                abort(400, message="license is already activated, please de-active first")

            transaction.active = True

            db.session.add(transaction)
            db.session.commit()

            GenericMessageSchema.message = "License is activated"

            return GenericMessageSchema


@blp.route("/license/deactivate")
class DeactivateLicense(MethodView):

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {"lic"}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @jwt_required()
    @blp.response(200, GenericMessageSchema)
    def post(self):
        if 'lic_file' not in request.files:
            return abort(400, message="lic_file is not provided")

        lic_file = request.files['lic_file']

        if lic_file.filename == '':
            return abort(400, message="file name is not provided")
        if lic_file and ActivateLicense.allowed_file(lic_file.filename):
            request_file = io.BytesIO(EncDec().decrypt_file_data(lic_file.stream.read()))
            request_data = json.load(request_file)

            transaction = TransactionModel.query.get_or_404(request_data["id"])

            UserModel.query.get_or_404(request_data["user_id"])
            ProductModel.query.get_or_404(request_data["product_id"])
            VersionModel.query.get_or_404(request_data["version_id"])

            if datetime.datetime.strptime(request_data["expired_on"],
                                          "%Y-%m-%d %H:%M:%S.%f") <= datetime.datetime.now():
                abort(400, message="license is expired on {}".format(request_data["expired_on"]))

            if not transaction.active:
                abort(400, message="license is not already activated, please active it first")

            transaction.active = False

            db.session.add(transaction)
            db.session.commit()

            GenericMessageSchema.message = "License is de-activated"

            return GenericMessageSchema
