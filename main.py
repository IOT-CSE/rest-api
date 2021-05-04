import json
from flask import Flask, jsonify, request, Response
from db import init_db, insert_product, find_products, find_product_by_id, update_product, delete_product


app = Flask(__name__)

products = [
    {"name": "chocolate", "price": 10, "category": "food"},
    {"name": "tv", "price": 10, "category": "electronics"},
    {"name": "socks", "price": 10, "category": "dress"}
]

init_db()

for product in products:
    insert_product(product)


@app.route('/products')
def list_producst():
    category = request.args.get('category')

    products = find_products(category=category)
    return jsonify(products)


@app.route('/products/<int:product_id>')
def product(product_id):
    product = find_product_by_id(product_id)

    if product is None:
        return jsonify(), 404

    return jsonify(product)


@app.route('/products', methods=['POST'])
def insert():

    product = request.json
    insert_product(product)

    return jsonify(product), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update(product_id):

    product = request.json
    updated_product = update_product(product_id, product)

    return jsonify(updated_product)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    delete_product(product_id)
    return jsonify(), 204
