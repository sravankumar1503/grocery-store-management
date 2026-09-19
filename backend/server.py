from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json
import os

import products_dao
import orders_dao
import uom_dao
import auth_dao
from auth import create_token, login_required

app = Flask(__name__)  

connection = get_sql_connection()

@app.route('/signup', methods=['POST'])
def signup():
    request_payload = json.loads(request.form['data'])
    username = request_payload.get('username', '').strip()
    password = request_payload.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing = auth_dao.get_user_by_username(connection, username)
    if existing:
        return jsonify({'error': 'Username already taken'}), 400

    user_id = auth_dao.create_user(connection, username, password)
    token = create_token(user_id, username)
    response = jsonify({'token': token, 'username': username})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/login', methods=['POST'])
def login():
    request_payload = json.loads(request.form['data'])
    username = request_payload.get('username', '').strip()
    password = request_payload.get('password', '')

    user = auth_dao.get_user_by_username(connection, username)
    if user is None or not auth_dao.check_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = create_token(user['user_id'], user['username'])
    response = jsonify({'token': token, 'username': user['username']})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
@login_required
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
@login_required
def get_products():
    response = products_dao.get_all_products(connection, request.user_id)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
@login_required
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload, request.user_id)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertUOM', methods=['POST'])
@login_required
def insert_uom():
    request_payload = json.loads(request.form['data'])
    uom_id = uom_dao.insert_new_uom(connection, request_payload)
    response = jsonify({
        'uom_id': uom_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
@login_required
def get_all_orders():
    response = orders_dao.get_all_orders(connection, request.user_id)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
@login_required
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload, request.user_id)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
@login_required
def delete_product():
    products_dao.delete_product(connection, request.form['product_id'], request.user_id)
    response = jsonify({
        'product_id': request.form['product_id']
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#new
@app.route('/updateProduct', methods=['POST'])
@login_required
def update_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.update_product(connection, request_payload, request.user_id)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertUOM', methods=['POST'])
@login_required
def insert_uom():
    request_payload = json.loads(request.form['data'])
    uom_id = uom_dao.insert_new_uom(connection, request_payload)
    response = jsonify({
        'uom_id': uom_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getOrderDetails', methods=['GET'])
@login_required
def get_order_details():
    order_id = request.args.get('order_id')
    response = orders_dao.get_order_details(connection, order_id, request.user_id)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/setupUsersTable', methods=['GET'])
def setup_users_table():
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL
            );
        """)
        conn.commit()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return jsonify({'status': 'done', 'tables_now': tables})
    except Exception as e:
        return jsonify({'error': str(e)})

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