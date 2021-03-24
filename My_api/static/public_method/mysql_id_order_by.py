"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/24 14:37
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : mysql_id_order_by.py
@Software  : PyCharm
"""

import pymysql
from icecream import ic


def mysql_id_order_by(table_data):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user="root",
        password="root",
        database="django_platform"
    )
    ads = 'id'
    cursor = db.cursor()
    # sql = f"SELECT * FROM login_user where username = '{IDS['user']}' AND password = '{IDS['pwd']}' AND is_delete = 0;"
    sql1 = f"ALTER TABLE {table_data} DROP {ads};"
    sql2 = f"ALTER TABLE {table_data} ADD {ads} int NOT NULL FIRST;"
    sql3 = f"ALTER TABLE {table_data} MODIFY COLUMN {ads} int NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY({ads});"
    ic(sql1)
    cursor.execute(sql1)
    db.commit()
    cursor.execute(sql2)
    db.commit()
    cursor.execute(sql3)
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    table_data = 'user_token'
    mysql_id_order_by(table_data)
