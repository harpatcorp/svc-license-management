import uuid

from sqldb import db


class ProductModel(db.Model):
    __tablename__ = "Product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=True)
    versions = db.relationship("VersionModel", back_populates="product", lazy="dynamic")
    image = db.Column(db.String, unique=False, nullable=True)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)
    modified_on = db.Column(db.DateTime, unique=False, nullable=True)
