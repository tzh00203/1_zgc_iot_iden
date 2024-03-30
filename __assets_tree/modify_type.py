import mysql.connector
from mysql_conf import cursor

def select_type(type_id=None, type_name=None):
    try:

        if type_id:
            query = "SELECT * FROM `type` WHERE id = {type_id}"
            cursor.execute(query)
        elif type_name:
            query = f"SELECT * FROM type WHERE name = '{type_name}'"
            cursor.execute(query)
        else:
            query = "SELECT * FROM type"
            cursor.execute(query)

        # 打印查询结果
        for (id, name) in cursor:
            print(f"id: {id}, name: {name}")

    except Exception as e:
        print(e)