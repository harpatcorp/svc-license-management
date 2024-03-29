import datetime
import os
import base64
import shutil
import uuid

from flask.views import MethodView
from flask import current_app as app
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from sqldb import db
from toolkit import isBase64
from models import ProductModel
from schema import ProductSchema, ProductInsertSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config import IMG_PATH


blp = Blueprint("Product", __name__, description="Business central extensions as a product")


@blp.route("/product/<string:product_id>")
class Product(MethodView):
    
    @blp.response(200, ProductInsertSchema)
    def get(self, product_id):
        '''
            This endpoint is used to retrive a product details based to product id
        '''
        app.logger.info("Product Id: {}".format(product_id))
        product = ProductModel.query.get_or_404(product_id)

        image = []

        if product.image is not None:
            for file in os.listdir(str(product.image)):
                if file.endswith(".jpeg"):
                    file_path = f"{product.image}/{file}"
                    with open(file_path, 'rb') as f:
                        image.append(base64.b64encode(f.read()).decode('utf-8'))

        product.image = image

        return product

    @jwt_required()
    @blp.arguments(ProductInsertSchema)
    @blp.response(200, ProductSchema)
    def patch(self, product_data, product_id):
        '''
            This is end point is used to update product details
            Note: Admin access is required
        '''
        app.logger.info("Product Id: {}".format(product_id))
        app.logger.info("Product Data: {}".format(product_data))
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        product = ProductModel.query.get_or_404(product_id)

        product.name = product_data["name"]
        product.description = product_data["description"]

        try:
            if len(product_data["image"]) > 5:
                app.logger.info("Length of image should be less or equal 5")
                abort(422, message="image should be less or equal 5")
            else:
                product_images = product_data["image"]
                product.image = str(product_images)

                if os.path.exists(str(product_images)):
                    shutil.rmtree(product_images)
                else:
                    product_images = os.path.join(IMG_PATH, str(uuid.uuid4()))
                    product.image = str(product_images)
                    os.makedirs(product_images)

                i = 1

                for image in product_data["image"]:
                    if not isBase64(str(image)):
                        abort(400, message="Image is not converted in base64.")
                    decoded_data = base64.b64decode(image)
                    img_file = open(str(product_images) + "/" + str(i) + ".jpeg", 'wb')
                    img_file.write(decoded_data)
                    img_file.close()
                    i = i + 1
        except KeyError:
            app.logger.info("image key not found")

        product.modified_on = datetime.datetime.now()

        db.session.add(product)
        db.session.commit()
        
        app.logger.info("Product {} is updated successfully.".format(product_id))
        
        return product

    @jwt_required()
    @blp.response(204)
    def delete(self, product_id):
        '''
            This end point is used to delete product and its available versions
            Note: Admin access is required
        '''
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        product = ProductModel.query.get_or_404(product_id)

        db.session.delete(product)
        db.session.commit()

        app.logger.info("Product {} is deleted".format(product_id))

        return 204


@blp.route("/product")
class ProductList(MethodView):

    @jwt_required()
    @blp.arguments(ProductInsertSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        '''
            This end point is used to upload product details
            Note: Admin access is required
        '''
        app.logger.info("Product Data: {}".format(product_data))
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            app.logger.info("Admin privilege required")
            abort(401, message="Admin privilege required.")

        product = ProductModel(**product_data)

        try:
            if len(product_data["image"]) > 5:
                app.logger.info("Length of image should be less or equal 5")
                abort(422, message="image should be less or equal 5")
            else:
                product_images = os.path.join(IMG_PATH, str(uuid.uuid4()))
                product.image = str(product_images)

                os.makedirs(product_images)

                i = 1

                for image in product_data["image"]:
                    if not isBase64(str(image)):
                        abort(400, message="Image is not converted in base64.")
                    decoded_data = base64.b64decode(image)

                    img_file = open(str(product_images)+"/"+str(i)+".jpeg", 'wb')
                    img_file.write(decoded_data)
                    img_file.close()

                    app.logger.info("Image {} is saved".format(i))
                    i = i + 1
        except KeyError:
            app.logger.info("Image key not found")

        product.created_on = datetime.datetime.now()
        product.modified_on = datetime.datetime.now()

        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Product is already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the product")
        
        app.logger.info("Product has been successfully uploaded")
        
        return product

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        '''
            This end point is used to retrive the list of available products
        '''
        products = ProductModel.query.all()
        return products
