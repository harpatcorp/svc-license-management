from sqldb import db


class TransactionModel(db.Model):
    __tablename__ = "Transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, unique=False, nullable=False)
    version_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    currency = db.Column(db.String(3), unique=False, nullable=False, default="INR")
    qty = db.Column(db.Float(precision=2), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    total_amt = db.Column(db.Float(precision=2), unique=False, nullable=False)
    order_id = db.Column(db.String(250), unique=False, nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=True)
    ordered_on = db.Column(db.DateTime)
    expired_on = db.Column(db.DateTime)
