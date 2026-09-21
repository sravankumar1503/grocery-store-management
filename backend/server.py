from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
from flask_cors import CORS
import mysql.connector
import json
import os

import products_dao
import orders_dao
import uom_dao
import auth_dao
import otp_dao
from email_service import send_otp_email
from auth import create_token, login_required

app = Flask(__name__)
CORS(app)

@app.route('/setupOtpTable', methods=['GET'])
def setup_otp_table():
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otp_verifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                is_verified TINYINT(1) NOT NULL DEFAULT 0,
                expires_at DATETIME NOT NULL,
                created_at DATETIME NOT NULL
            );
        """)
        conn.commit()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return jsonify({'status': 'done', 'tables_now': tables})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/sendOtp', methods=['POST'])
def send_otp():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    email = request_payload.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'error': 'Please enter a valid email address'}), 400

    existing_user = auth_dao.get_user_by_username(connection, email)
    if existing_user:
        return jsonify({'error': 'An account with this email already exists'}), 400

    otp_code = otp_dao.create_otp(connection, email)

    try:
        send_otp_email(email, otp_code)
    except Exception as e:
        return jsonify({'error': 'Could not send the verification email. Please try again.'}), 500

    response = jsonify({'status': 'sent'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/verifyOtp', methods=['POST'])
def verify_otp():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    email = request_payload.get('email', '').strip().lower()
    otp_code = request_payload.get('otp', '').strip()

    ok, error = otp_dao.verify_otp(connection, email, otp_code)
    if not ok:
        return jsonify({'error': error}), 400

    response = jsonify({'status': 'verified'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/signup', methods=['POST'])
def signup():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    username = request_payload.get('username', '').strip().lower()
    password = request_payload.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if not otp_dao.is_email_verified_recently(connection, username):
        return jsonify({'error': 'Please verify your email before creating an account'}), 400

    existing = auth_dao.get_user_by_username(connection, username)
    if existing:
        return jsonify({'error': 'An account with this email already exists'}), 400

    user_id = auth_dao.create_user(connection, username, password)
    otp_dao.clear_otp(connection, username)
    token = create_token(user_id, username)
    response = jsonify({'token': token, 'username': username})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/login', methods=['POST'])
def login():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    username = request_payload.get('username', '').strip()
    password = request_payload.get('password', '')

    user = auth_dao.get_user_by_username(connection, username)
    if user is None or not auth_dao.check_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = create_token(user['user_id'], user['username'])
    response = jsonify({'token': token, 'username': user['username']})
    return response


@app.route('/whoami', methods=['GET'])
@login_required
def whoami():
    response = jsonify({'user_id': request.user_id})
    return response


@app.route('/getUOM', methods=['GET'])
@login_required
def get_uom():
    connection = get_sql_connection()
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    return response


@app.route('/insertUOM', methods=['POST'])
@login_required
def insert_uom():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    uom_id = uom_dao.insert_new_uom(connection, request_payload)
    response = jsonify({
        'uom_id': uom_id
    })
    return response


@app.route('/getProducts', methods=['GET'])
@login_required
def get_products():
    connection = get_sql_connection()
    response = products_dao.get_all_products(connection, request.user_id)
    response = jsonify(response)
    return response


@app.route('/insertProduct', methods=['POST'])
@login_required
def insert_product():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload, request.user_id)
    response = jsonify({
        'product_id': product_id
    })
    return response


@app.route('/updateProduct', methods=['POST'])
@login_required
def update_product():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.update_product(connection, request_payload, request.user_id)
    response = jsonify({
        'product_id': product_id
    })
    return response

    try:
        conn = get_sql_connection()
        cursor = conn.cursor()

        # Clear any leftover test data first, since existing rows can't get a NOT NULL user_id automatically
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        cursor.execute("DELETE FROM order_details;")
        cursor.execute("DELETE FROM orders;")
        cursor.execute("DELETE FROM products;")
        conn.commit()

        results = {}

        try:
            cursor.execute("ALTER TABLE products ADD COLUMN user_id INT NOT NULL;")
            conn.commit()
            results['products_column'] = 'added'
        except Exception as e:
            results['products_column'] = str(e)

        try:
            cursor.execute("ALTER TABLE products ADD FOREIGN KEY (user_id) REFERENCES users(user_id);")
            conn.commit()
            results['products_fk'] = 'added'
        except Exception as e:
            results['products_fk'] = str(e)

        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN user_id INT NOT NULL;")
            conn.commit()
            results['orders_column'] = 'added'
        except Exception as e:
            results['orders_column'] = str(e)

        try:
            cursor.execute("ALTER TABLE orders ADD FOREIGN KEY (user_id) REFERENCES users(user_id);")
            conn.commit()
            results['orders_fk'] = 'added'
        except Exception as e:
            results['orders_fk'] = str(e)

        cursor.execute("DESCRIBE products;")
        products_desc = cursor.fetchall()
        cursor.execute("DESCRIBE orders;")
        orders_desc = cursor.fetchall()

        return jsonify({
            'results': results,
            'products_columns': products_desc,
            'orders_columns': orders_desc
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/getAllOrders', methods=['GET'])
@login_required
def get_all_orders():
    connection = get_sql_connection()
    response = orders_dao.get_all_orders(connection, request.user_id)
    response = jsonify(response)
    return response


@app.route('/getOrderDetails', methods=['GET'])
@login_required
def get_order_details():
    connection = get_sql_connection()
    order_id = request.args.get('order_id')
    response = orders_dao.get_order_details(connection, order_id, request.user_id)
    response = jsonify(response)
    return response


@app.route('/insertOrder', methods=['POST'])
@login_required
def insert_order():
    connection = get_sql_connection()
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload, request.user_id)
    response = jsonify({
        'order_id': order_id
    })
    return response


@app.route('/deleteProduct', methods=['POST'])
@login_required
def delete_product():
    connection = get_sql_connection()
    products_dao.delete_product(connection, request.form['product_id'], request.user_id)
    response = jsonify({
        'product_id': request.form['product_id']
    })
    return response

@app.route('/getOrderReceipt', methods=['GET'])
@login_required
def get_order_receipt():
    connection = get_sql_connection()
    order_id = request.args.get('order_id')
    receipt = orders_dao.get_order_receipt(connection, order_id, request.user_id)
    if receipt is None:
        return jsonify({'error': 'Order not found'}), 404
    response = jsonify(receipt)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)