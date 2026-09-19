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

@app.route('/debugConfig', methods=['GET'])
def debug_config():
    return jsonify({
        'DB_HOST': os.environ.get('DB_HOST'),
        'DB_NAME': os.environ.get('DB_NAME'),
        'DB_USER': os.environ.get('DB_USER'),
        'DB_PORT': os.environ.get('DB_PORT')
    })

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