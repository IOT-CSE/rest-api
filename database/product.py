from database.db import db
# in order to init table
from database.category import Category


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)

    category = db.relationship('Category',
                               backref=db.backref('product', lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category.name
        }


def getProducts(filter=None):
    category = None

    if 'category' in filter:
        category = filter['category']
        filter.pop('category', None)

    products = Product.query.filter_by(**filter)

    if category is not None:
        products = products.filter(
            Product.category.has(name=category))

    return [p.serialize for p in products]


def insertProduct(product):
    insertedProduct = Product(**product)
    db.session.add(insertedProduct)
    db.session.commit()

    return insertedProduct.serialize


def updateProduct(id, product):
    Product.query.filter_by(id=id).update(product)

    db.session.commit()

    return getProducts({"id": id})[0]


def deleteProduct(id):
    Product.query.filter_by(id=id).delete()

    db.session.commit()
