import mysql.connector
from mysql_conf import mysql_config


def select_product(product_id=None, product_name=None, vendor_id=None, type_id=None):
    try:
        # 建立连接
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()

        # 执行查询
        if product_id:
            query = f"SELECT * FROM product WHERE id = {product_id}"
            cursor.execute(query)
        elif product_name:
            query = f"SELECT * FROM product WHERE name = '{product_name}'"
            cursor.execute(query)

        # 打印查询结果
        for (id, name, vendor_id, type_id) in cursor:
            print(f"id: {id}, name: {name}, vendor_id: {vendor_id}, type_id: {type_id}")

    finally:
        # 关闭连接
        cursor.close()
        cnx.close()
