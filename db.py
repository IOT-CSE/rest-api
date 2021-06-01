from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5432/test'
    db.init_app(app)
    Migrate(app,db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    @property
    def serialize(self):
       return {
           'id': self.id,
           'name': self.name,
           'price' : self.price
       }
    

def getProducts():
    return [p.serialize for p in Product.query.all()]

def getProductById(id):
    prod = Product.query.filter_by(id = id).first()
    if prod is not None :
        prod = prod.serialize
    return prod

def getProductByCategory(category):
    return [p.serialize for p in Product.query.filter_by(category = category)]

def insertProduct(_product):
    product = Product(name=_product['name'],price=_product['price'])
    db.session.add(product)
    db.session.commit()

    return product.serialize
