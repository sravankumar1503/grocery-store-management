import os

from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json
import os

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)  

connection = get_sql_connection()

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/setupTables', methods=['GET'])
def setup_tables():
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uom (
                uom_id INT AUTO_INCREMENT PRIMARY KEY,
                uom_name VARCHAR(255) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                uom_id INT NOT NULL,
                price_per_unit DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                datetime DATETIME NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity DECIMAL(10,2) NOT NULL,
                total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

        conn.commit()

        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return jsonify({'status': 'done', 'tables_now': tables})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#new
@app.route('/updateProduct', methods=['POST'])
def update_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.update_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertUOM', methods=['POST'])
def insert_uom():
    request_payload = json.loads(request.form['data'])
    uom_id = uom_dao.insert_new_uom(connection, request_payload)
    response = jsonify({
        'uom_id': uom_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getOrderDetails', methods=['GET'])
def get_order_details():

    order_id = request.args.get('order_id')

    print("ORDER ID:", order_id)

    response = orders_dao.get_order_details(connection, order_id)

    print("ORDER DETAILS:", response)

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
'''
@app.route('/getOrderDetails', methods=['GET'])
def get_order_details():
    order_id = request.args.get('order_id')
    response = orders_dao.get_order_details(connection, order_id)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response'''

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)