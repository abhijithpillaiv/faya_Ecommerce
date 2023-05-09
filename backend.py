import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

db_name="faya_ecommerce2"
# Create a connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abhi262001",
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS "+db_name)
db.database=db_name
app = Flask(__name__)
CORS(app)
#***************************************************************************************************************

# Customer API

# Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        return jsonify(customers)
    except:
        return("No data found.")

# Add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    # Check if table exists, create it if not
    cursor.execute("SHOW TABLES LIKE 'customers'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('CREATE TABLE customers (name VARCHAR(255) NOT NULL, email VARCHAR(255) PRIMARY KEY, address VARCHAR(255) NOT NULL)')
        db.commit()

    cursor.execute('INSERT INTO customers (name, email, address) VALUES (%s, %s, %s)', (name, email, address))
    db.commit()
    return 'Customer added'

# Update a customer
@app.route('/customers/<string:email>', methods=['PUT'])
def update_customer(email):
    # Check if email exists in database
    cursor.execute('SELECT * FROM customers WHERE email=%s', (email,))
    result = cursor.fetchone()
    if result is None:
        return 'Email not found', 404
    name = request.form['name']
    address = request.form['address']
    cursor.execute('UPDATE customers SET name=%s,  address=%s WHERE email=%s', (name, address, email))
    db.commit()
    return 'Your details are updated'

# Delete a customer
@app.route('/customers/<string:email>', methods=['DELETE'])
def delete_customer(email):
    # Check if customer exists
    cursor.execute('SELECT * FROM customers WHERE email=%s', (email,))
    if cursor.fetchone() is None:
        return 'Customer not found', 404
    
    cursor.execute('DELETE FROM customers WHERE email=%s', (email,))
    db.commit()
    return 'Customer deleted'

#***************************************************************************************************************

# API for products

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    try:
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        return jsonify(products)
    except:
        return("No data found.")

# Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    customer_email = request.form['customer_email']
    TimeStamp = datetime.now()

    # Check if email exists in database
    cursor.execute('SELECT * FROM customers WHERE email=%s', (customer_email,))
    result = cursor.fetchone()
    if result is None:
        return 'Customer email not found in database', 404
    
    # Check if table exists, create it if not
    cursor.execute("SHOW TABLES LIKE 'products'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, customer_email VARCHAR(255), price INT NOT NULL, TimeStamp VARCHAR(255) NOT NULL, active BOOLEAN DEFAULT TRUE)')
        db.commit()
    
    cursor.execute('INSERT INTO products (name, price, customer_email, TimeStamp) VALUES (%s, %s, %s, %s)', (name, price, customer_email, TimeStamp))
    db.commit()
    
    return 'Product added'


# Update a product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    name = request.form['name']
    price = request.form['price']

    # Check if product exists in database
    cursor.execute('SELECT * FROM products WHERE id=%s', (id,))
    result = cursor.fetchone()
    if result is None:
        return 'product not found', 404
    cursor.execute('UPDATE products SET name=%s, price=%s WHERE id=%s', (name, price,  id))
    db.commit()
    return 'Product updated'

# Delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    # Check if product exists in database
    cursor.execute('SELECT * FROM products WHERE id=%s', (id,))
    result = cursor.fetchone()
    if result is None:
        return 'product not found', 404
    cursor.execute('DELETE FROM products WHERE id=%s', (id,))
    db.commit()
    return 'Product deleted'


# product activation
@app.route('/products/<int:id>/<int:status>', methods=['PUT'])
def update_product_status(id,status):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products WHERE id=%s', (id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({'message': 'Product not found'}), 404
    
    created_date = datetime.fromisoformat(result['TimeStamp'])
    current_date = datetime.now()
    time_diff = (current_date - created_date).days
    if time_diff >= 60:
        cursor.execute('UPDATE products SET active=%s WHERE id=%s', (bool(status), id))
        db.commit()
        return jsonify({'message': f'Product {"deactivated" if not status else "activated"} successfully'}), 200
    else:
        return jsonify({'message': f'Product can only be deactivated after {60-time_diff} days'}), 403

if __name__ == "__main__":
    app.run(port=8000)