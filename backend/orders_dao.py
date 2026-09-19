from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
  cursor = connection.cursor()
  insert_order_query = ("INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")
  order_data = (order['customer_name'], order['total'], datetime.now())
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

def get_all_orders(connection):
  cursor = connection.cursor()
  query = ("SELECT * FROM orders")
  cursor.execute(query)
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


def get_order_details(connection, order_id):
  cursor = connection.cursor()
  query = ("SELECT order_details.product_id, products.name, order_details.quantity, order_details.total_price "
           "FROM order_details INNER JOIN products ON order_details.product_id = products.product_id "
           "WHERE order_details.order_id = %s")
  cursor.execute(query, (order_id,))
  details = []
  for (product_id, name, quantity, total_price) in cursor:
    details.append({
      'product_id': product_id,
      'product_name': name,
      'quantity': quantity,
      'total_price': total_price
    })
  return details

if __name__ == "__main__":
  connection = get_sql_connection()
  print(get_all_orders(connection))