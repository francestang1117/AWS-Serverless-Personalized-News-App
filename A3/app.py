from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin1234@my-rds-test-instance-1.cijvhyi4y3jw.us-east-1.rds.amazonaws.com:3306/mydb'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    name = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.String(100))
    availability = db.Column(db.Boolean)

    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        self.availability = availability

@app.route('/store-products', methods = ['POST'])
def store():

    try:

        data = request.get_json()
        products = data['products']

        for product in products:
            name = product['name']
            price = product['price']
            availability = product['availability']

            newProduct = Product(name, price, availability)
            db.session.add(newProduct)

        db.session.commit()

        return jsonify({'message': 'Success.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/list-products')
def list_products():
    try:
        products = Product.query.all()
        productsList = [{'name': product.name, 'price': product.price, 'availability': product.availability} for product in products]

        return jsonify({'products': productsList}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)