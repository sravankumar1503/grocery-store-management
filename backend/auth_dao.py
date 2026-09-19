from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


def create_user(connection, username, password):
    cursor = connection.cursor()
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    query = ("INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)")
    cursor.execute(query, (username, password_hash, datetime.now()))
    connection.commit()
    return cursor.lastrowid


def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = ("SELECT user_id, username, password_hash FROM users WHERE username = %s")
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    if row is None:
        return None
    return {'user_id': row[0], 'username': row[1], 'password_hash': row[2]}


def check_password(password, password_hash):
    return bcrypt.check_password_hash(password_hash, password)