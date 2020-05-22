from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


# Init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Model of the product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sku = db.Column(db.String(100))
    group = db.Column(db.String(100))
    balance = db.Column(db.Integer)

    def __init__(self, name, sku, group, balance):
        self.name = name
        self.sku = sku
        self.group = group
        self.balance = balance

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'sku', 'group', 'balance')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    sku = request.json['sku']
    group = request.json['group']
    balance = request.json['balance']
    
    new_product = Product(name, sku, group, balance)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all of the products 
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    sku = request.json['sku']
    group = request.json['group']
    balance = request.json['balance']

    product.name = name
    product.sku = sku
    product.group = group
    product.balance = balance

    db.session.commit()

    return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server btw check this out https://www.youtube.com/watch?v=sugvnHA7ElY&t=26s
if __name__ == '__main__':
    app.run(debug=True)