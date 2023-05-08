import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

# Create a connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abhi262001",
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
app = Flask(__name__)
CORS(app)
#***************************************************************************************************************

# Customer API

# Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    return jsonify(customers)

# Add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data['name']
    email = data['email']
    address = data['address']
    cursor.execute('INSERT INTO customers (name, email, address) VALUES (%s, %s, %s)', (name, email, address))
    db.commit()
    return 'Customer added'

# Update a customer
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    address = data['address']
    cursor.execute('UPDATE customers SET name=%s, email=%s, address=%s WHERE id=%s', (name, email, address, id))
    db.commit()
    return 'Your details are updated'

# Delete a customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    cursor.execute('DELETE FROM customers WHERE id=%s', (id,))
    db.commit()
    return 'Customer deleted'

#***************************************************************************************************************

# API for products

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return jsonify(products)

# Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data['name']
    price = data['price']
    customer_id = data['customer_id']
    TimeStrap=datetime.now()
    cursor.execute('INSERT INTO products (name, price, customer_id,TimeStrap) VALUES (%s, %s, %s)', (name, price, customer_id,TimeStrap))
    db.commit()
    return 'Product added'

# Update a product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    name = data['name']
    price = data['price']
    customer_id = data['customer_id']
    cursor.execute('UPDATE products SET name=%s, price=%s, customer_id=%s WHERE id=%s', (name, price, customer_id, id))
    db.commit()
    return 'Product updated'

# Delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    cursor.execute('DELETE FROM products WHERE id=%s', (id,))
    db.commit()
    return 'Product deleted'


#product activation
@app.route('/products/<int:id>/status', methods=['PUT'])
def update_product_status(id):
    cursor.execute('SELECT * FROM products WHERE id=%s', (id,))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return jsonify({'message': 'Product not found'})
    created_date = result['TimeStrap']
    current_date = datetime.now()
    time_diff = current_date - created_date
    if time_diff < 60:
        cursor.execute('UPDATE products SET active=%s WHERE id=%s', (False, id))
        db.commit()
        return jsonify({'message': 'Product deactivated successfully'})
    else:
        return jsonify({'message': 'Product can only be deactivated after'+(60-time_diff)+'days'})

if __name__ == "__main__":
    app.run(port=8000)