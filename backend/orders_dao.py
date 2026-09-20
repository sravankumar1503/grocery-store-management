from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order, user_id):
  cursor = connection.cursor()
  insert_order_query = ("INSERT INTO orders (customer_name, total, datetime, user_id) VALUES (%s, %s, %s, %s)")
  order_data = (order['customer_name'], order['total'], datetime.now(), user_id)
  cursor.execute(insert_order_query, order_data)
  order_id = cursor.lastrowid

  order_details_query = ("INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
  order_details_data = []
  for order_detail_record in order['order_details']:
    order_details_data.append([
      order_id, 
      int(order_detail_record['product_id']), 
      float(order_detail_record['quantity']), 
      float(order_detail_record['total_price'])
      ])

  cursor.executemany(order_details_query, order_details_data)
  connection.commit()
  return order_id

def get_all_orders(connection, user_id):
  cursor = connection.cursor()
  query = ("SELECT order_id, customer_name, total, datetime FROM orders WHERE user_id = %s")
  cursor.execute(query, (user_id,))
  orders = []
  for (order_id, customer_name, total, datetime) in cursor:
    order = {
      'order_id': order_id,
      'customer_name': customer_name,
      'total': total,
      'datetime': datetime
    }
    orders.append(order)
  return orders


def get_order_details(connection, order_id, user_id):
  cursor = connection.cursor()
  # The join to `orders` here also enforces that this order_id actually belongs
  # to this user_id - without it, anyone could pass any order_id and see it.
  query = ("SELECT order_details.product_id, products.name, order_details.quantity, order_details.total_price "
           "FROM order_details "
           "INNER JOIN products ON order_details.product_id = products.product_id "
           "INNER JOIN orders ON order_details.order_id = orders.order_id "
           "WHERE order_details.order_id = %s AND orders.user_id = %s")
  cursor.execute(query, (order_id, user_id))
  details = []
  for (product_id, name, quantity, total_price) in cursor:
    details.append({
      'product_id': product_id,
      'product_name': name,
      'quantity': quantity,
      'total_price': total_price
    })
  return details

def get_order_receipt(connection, order_id, user_id):
  cursor = connection.cursor()

  header_query = ("SELECT customer_name, datetime, total FROM orders WHERE order_id = %s AND user_id = %s")
  cursor.execute(header_query, (order_id, user_id))
  header_row = cursor.fetchone()
  if header_row is None:
    return None

  header = {
    'customer_name': header_row[0],
    'datetime': header_row[1],
    'total': header_row[2]
  }

  items_query = ("SELECT products.name, order_details.quantity, products.price_per_unit, order_details.total_price "
                  "FROM order_details "
                  "INNER JOIN products ON order_details.product_id = products.product_id "
                  "INNER JOIN orders ON order_details.order_id = orders.order_id "
                  "WHERE order_details.order_id = %s AND orders.user_id = %s")
  cursor.execute(items_query, (order_id, user_id))
  items = []
  for (name, quantity, act_price, total_price) in cursor:
    items.append({
      'product_name': name,
      'quantity': quantity,
      'act_price': act_price,
      'total_price': total_price
    })

  header['items'] = items
  return header

if __name__ == "__main__":
  connection = get_sql_connection()
  print(get_all_orders(connection, 1))