import json
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from db import getProductById, getProducts, init_db, Product, insertProduct
# from db import init_db, insert_product, find_products, find_product_by_id, update_product, delete_product


app = Flask(__name__)
init_db(app)

@app.route('/products')
def list_producst():
    return jsonify(getProducts())


@app.route('/products/<int:product_id>')
def product(product_id):
    try:
        product = getProductById(product_id)

        if product is None:
            return jsonify(), 404

        return jsonify(product)
    except Exception as e:
        return returnFailedOperation(e,400)


@app.route('/products', methods=['POST'])
def insert():
    try:
        return jsonify(insertProduct(request.json)), 201
    except Exception as e:
        return returnFailedOperation(e,400)


# @app.route('/products/<int:product_id>', methods=['PUT'])
# def update(product_id):

#     product = request.json
#     updated_product = update_product(product_id, product)

#     return jsonify(updated_product)


# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete(product_id):
#     delete_product(product_id)
#     return jsonify(), 204

def returnFailedOperation(e,code):
    return {"message":"Operation failed. " + str(e)}, code

