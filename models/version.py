from sqldb import db


class VersionModel(db.Model):
    __tablename__ = "Version"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), unique=False, nullable=False)
    product = db.relationship("ProductModel", back_populates="versions")
    tag = db.Column(db.String(50), unique=False, nullable=False)
    currency = db.Column(db.String(3), unique=False, nullable=False, default="USD")
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    path = db.Column(db.String, unique=False, nullable=True)
    created_on = db.Column(db.DateTime)
    modified_on = db.Column(db.DateTime)
    u_tag = db.UniqueConstraint(product_id, tag)
