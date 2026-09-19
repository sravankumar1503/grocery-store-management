import os
import mysql.connector

try:
    import config
except ImportError:
    config = None

__cnx = None


def _create_connection():
    return mysql.connector.connect(
        user=os.environ.get('DB_USER', config.DB_USER if config else None),
        password=os.environ.get('DB_PASSWORD', config.DB_PASSWORD if config else None),
        host=os.environ.get('DB_HOST', config.DB_HOST if config else None),
        port=int(os.environ.get('DB_PORT', 3306)),
        database=os.environ.get('DB_NAME', config.DB_NAME if config else None)
    )


def get_sql_connection():
    global __cnx
    if __cnx is None or not __cnx.is_connected():
        __cnx = _create_connection()
    return __cnx