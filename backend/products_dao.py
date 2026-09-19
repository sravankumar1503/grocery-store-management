import mysql.connector
from sql_connection import get_sql_connection


def get_all_products(connection, user_id):
    cursor = connection.cursor()
    query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
              "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id "
              "WHERE products.user_id = %s")
    cursor.execute(query, (user_id,))

    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "uom_id": uom_id,
            "price_per_unit": price_per_unit,
            "uom_name": uom_name
        })
    return response


def insert_new_product(connection, product, user_id):
    cursor = connection.cursor()
    query = ("INSERT INTO products (name, uom_id, price_per_unit, user_id) VALUES (%s, %s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'], user_id)
    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid


def update_product(connection, product, user_id):
    cursor = connection.cursor()
    query = ("UPDATE products SET name = %s, uom_id = %s, price_per_unit = %s "
              "WHERE product_id = %s AND user_id = %s")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'], product['product_id'], user_id)
    cursor.execute(query, data)
    connection.commit()

    return product['product_id']


def delete_product(connection, product_id, user_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products WHERE product_id = %s AND user_id = %s")
    cursor.execute(query, (product_id, user_id))
    connection.commit()