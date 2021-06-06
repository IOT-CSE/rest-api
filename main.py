import json
import os

from flask import Flask, jsonify, request

from database.db import init_db
import database.category as Categories
import database.product as Products


app = Flask(__name__)
app = init_db(app)
app.app_context().push()

# insert rows
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, "files", "categories.json")) as file:
    categories = json.load(file)
    for category in categories:
        Categories.insert(category)

with open(os.path.join(__location__, "files", "products.json")) as file:
    products = json.load(file)
    for product in products:
        Products.insert(product)

# PRODUCTS # 


@app.route('/products')
def list_producst():
    try:
        products = Products.find(request.args.to_dict())

        if products is None:
            return jsonify([]), 404

        return jsonify(products)
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>')
def get_product(product_id):
    try:
        products = Products.find({"id": product_id})

        if products is None:
            return jsonify(), 404

        return jsonify(products[0])
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products', methods=['POST'])
def insert_product():
    try:
        product = Products.insert(request.json)
        return jsonify(product), 201
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    product = request.json

    try:
        updatedProduct = Products.update(product_id, product)

        return jsonify(updatedProduct), 200
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        Products.delete(product_id)
        return jsonify(), 204
    except Exception as e:
        return failedResponse(e, 400)

# CATEGORY # 


@app.route('/categories')
def list_categories():
    try:
        categories = Categories.find(request.args.to_dict())

        if categories is None:
            return jsonify([]), 404

        return jsonify(categories)
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/categories/<int:category_id>')
def get_category(category_id):
    try:
        categories = Categories.find({"id": category_id})

        if categories is None:
            return jsonify(), 404

        return jsonify(categories[0])
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/categories', methods=['POST'])
def insert_category():
    try:
        category = Categories.insert(request.json)
        return jsonify(category), 201
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):

    category = request.json

    try:
        updatedCategory = Categories.update(category_id, category)

        return jsonify(updatedCategory), 200
    except Exception as e:
        return failedResponse(e, 400)


@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        Categories.delete(category_id)
        return jsonify(), 204
    except Exception as e:
        return failedResponse(e, 400)


def failedResponse(e, code):
    return {"message": "Operation failed.", "reason": str(e)}, code
