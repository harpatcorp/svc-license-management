from sqldb import db


class UserModel(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password_1 = db.Column(db.String(50), unique=False, nullable=False)
    password_2 = db.Column(db.String(50), unique=False, nullable=False)
    otp_varified = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(db.DateTime)
