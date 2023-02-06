from sqldb import db


class VersionModel(db.Model):
    __tablename__ = "Version"

    id = db.Column(db.Integer, primary_key=True)
    # product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), unique=False, nullable=False)
    # product = db.relationship("ProductModel", back_populates="versions")
    tag = db.Column(db.String(80), unique=True, nullable=False)
    currency = db.Column(db.String(3), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    path = db.Column(db.String, unique=False, nullable=False)
    created_on = db.Column(db.DateTime)
    modified_on = db.Column(db.DateTime)
