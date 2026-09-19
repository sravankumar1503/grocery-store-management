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
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



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