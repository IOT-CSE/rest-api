import json
import os

from flask import Flask, jsonify, request

from database.db import init_db
from database.category import insertCategory
from database.product import deleteProduct, getProducts, insertProduct, updateProduct


app = Flask(__name__)
app = init_db(app)
app.app_context().push()

# insert rows
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, "files", "categories.json")) as file:
    categories = json.load(file)
    for category in categories:
        insertCategory(category)

with open(os.path.join(__location__, "files", "products.json")) as file:
    products = json.load(file)
    for product in products:
        insertProduct(product)


@app.route('/products')
def list_producst():
    try:
        products = getProducts(request.args.to_dict())

        if products is None:
            return jsonify([]), 404

        return jsonify(products)
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>')
def product(product_id):
    try:
        products = getProducts({"id": product_id})

        if products is None:
            return jsonify(), 404

        return jsonify(products[0])
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products', methods=['POST'])
def insert():
    try:
        product = insertProduct(request.json)
        return jsonify(product), 201
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>', methods=['PUT'])
def update(product_id):

    product = request.json

    try:
        updatedProduct = updateProduct(product_id, product)

        return jsonify(updatedProduct), 200
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    try:
        deleteProduct(product_id)
        return jsonify(), 204
    except Exception as e:
        return failedResponse(e, 400)


def failedResponse(e, code):
    return {"message": "Operation failed.", "reason": str(e)}, code
