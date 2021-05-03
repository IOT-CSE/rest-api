from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

products = [
    {"_id": 1, "name": "chocolate", "price": 10, "category": "food"},
    {"_id": 2, "name": "tv", "price": 10, "category": "electronics"},
    {"_id": 3, "name": "socks", "price": 10, "category": "dress"}
]


@app.route('/products')
def list_producst():

    category = request.args.get('category')
    if category == None:
        return jsonify(products)

    filtered_products = []

    for product in products:
        if product['category'] == category:
            filtered_products.append(product)

    return jsonify(filtered_products)


@app.route('/products/<int:product_id>')
def product(product_id):

    for product in products:
        if product['_id'] == product_id:
            return jsonify(product)

    return jsonify([]), 404


@app.route('/products', methods=['POST'])
def insert():

    product = request.json
    products.append(product)

    return jsonify(product), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update(product_id):

    product = request.json
    updated_product = request.json

    for i in range(len(products)):
        if products[i]['_id'] == product_id:
            products[i] = updated_product
            return jsonify(updated_product), 200

    return jsonify([]), 404


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    product = request.json

    for i in range(len(products)):
        if products[i]['_id'] == product_id:
            products.remove(products[i])
            return jsonify(), 204

    return jsonify([]), 404
